# -*- coding: utf-8 -*-

from odoo import api, models, fields, _
from re import findall as regex_findall, split as regex_split
from odoo.exceptions import ValidationError


class StockMove(models.Model):
    _inherit = 'stock.move'

    next_serial_qty = fields.Integer('Quantity per Lot')

    @api.model
    def create(self, vals):
        next_serial_qty = False
        product_uom_qty = vals.get('product_uom_qty')
        product_id = vals.get('product_id')
        tracking = 'none'
        if product_id:
            tracking = self.env['product.product'].browse(product_id).tracking
        if product_uom_qty and tracking == 'lot':
            serial_range = product_uom_qty / product_uom_qty
            vals.update({'next_serial_qty': product_uom_qty, 'next_serial_count': serial_range})
        elif product_uom_qty and tracking == 'serial':
            serial_range = product_uom_qty / 1
            vals.update({'next_serial_qty': 1, 'next_serial_count': serial_range})
        return super(StockMove, self).create(vals)

    @api.depends('has_tracking', 'picking_type_id.use_create_lots', 'picking_type_id.use_existing_lots', 'state')
    def _compute_display_assign_serial(self):
        for move in self:
            move.display_assign_serial = (
                move.has_tracking in ['serial', 'lot'] and
                move.state in ('partially_available', 'assigned', 'confirmed') and
                move.picking_type_id.use_create_lots and
                not move.picking_type_id.use_existing_lots
            )

    @api.onchange('next_serial_qty')
    def _onchange_next_serial_qty(self):
        if self.product_id and self.product_id.tracking == 'lot':
            serial_range = int(int(self.product_uom_qty) / self.next_serial_qty)
            self.next_serial_count = serial_range

    def _generate_serial_numbers(self, next_serial_count=False):
        """ This method will generate `lot_name` from a string (field
        `next_serial`) and create a move line for each generated `lot_name`.
        """
        self.ensure_one()

        if not next_serial_count:
            next_serial_count = self.next_serial_count

        # We look if the serial number contains at least one digit.
        caught_initial_number = regex_findall("\d+", self.next_serial)
        if not caught_initial_number:
            raise ValidationError(_('The serial number must contain at least one digit.'))
        # We base the serie on the last number find in the base serial number.
        initial_number = caught_initial_number[-1]
        padding = len(initial_number)
        # We split the serial number to get the prefix and suffix.
        splitted = regex_split(initial_number, self.next_serial)
        # initial_number could appear several times in the SN, e.g. BAV023B00001S00001
        prefix = initial_number.join(splitted[:-1])
        suffix = splitted[-1]
        initial_number = int(initial_number)
        serial_range = next_serial_count
        if self.product_id and self.product_id.tracking == 'lot':
            serial_range = int(int(self.product_uom_qty) / self.next_serial_qty)
            self.next_serial_count = serial_range
        lot_names = []
        # for i in range(0, next_serial_count):
        for i in range(0, serial_range):
            lot_names.append('%s%s%s' % (
                prefix,
                str(initial_number + i).zfill(padding),
                suffix
            ))
        move_lines_commands = self._generate_serial_move_line_commands(lot_names)
        if self.product_id and self.product_id.tracking == 'lot':
            for line in move_lines_commands:
                line_vals = line[2]
                if 'qty_done' in line_vals:
                    line_vals.update({'qty_done': self.next_serial_qty})
        self.write({'move_line_ids': move_lines_commands})
        return True