# -*- coding: utf-8 -*-

from odoo import api, models, fields, _
from re import findall as regex_findall, split as regex_split
from odoo.exceptions import UserError, ValidationError


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    has_tracking = fields.Selection(related='product_id.tracking', string='Product with Tracking')
    display_assign_serial = fields.Boolean(compute='_compute_display_assign_serial')
    next_serial = fields.Char('First SN')
    next_serial_count = fields.Integer('Number of SN', copy=False, help="Number of producing finished products per click.")
    next_serial_qty = fields.Integer('Quantity per Lot')
    move_line_component_ids = fields.One2many('move.line.component', 'production_id', string='Finished Products Components')
    is_components_created = fields.Boolean(string='Components Created?')

    # def write(self, vals):
    #     if vals.get('move_line_component_ids') and len(vals['move_line_component_ids']) == 1:
    #         vals.update({'is_components_created': False})
    #     return super(MrpProduction, self).write(vals)

    @api.onchange('has_tracking', 'product_qty')
    def _onchange_next_serial_count(self):
        self.next_serial_qty = 0
        self.next_serial_count = 0
        if self.has_tracking == 'lot':
            self.next_serial_count = 1
            self.next_serial_qty = self.product_qty
        if self.has_tracking == 'serial':
            self.next_serial_count = self.product_qty
            self.next_serial_qty = 1

    def generate_sequence_number(self):
        sequence_ref = self.env.ref('stock.sequence_production_lots')
        if self.state not in ['done', 'cancel'] and sequence_ref and \
                sequence_ref.number_next_actual and not self.next_serial:
            next_seq = sequence_ref.get_next_char(sequence_ref.number_next_actual)
            self.next_serial = next_seq

    @api.depends('has_tracking')
    def _compute_display_assign_serial(self):
        for mrp in self:
            mrp.display_assign_serial = (mrp.has_tracking in ['serial', 'lot'])

    def action_assign_serial_show_details(self):
        """ On `self.move_line_ids`, assign `lot_name` according to
        `self.next_serial` before returning `self.action_show_details`.
        """
        self.ensure_one()
        context = self._context.copy() or False
        if not self.next_serial:
            raise UserError(_("You need to set a Serial Number before generating more."))
        if self.state not in ['confirmed', 'planned', 'progress', 'to_close']:
            raise UserError(_("You need to confirm the Manufacturing order generating Serial Number."))
        if len(self.finished_move_line_ids.ids) > self.product_qty:
            raise UserError(_("Already produced all defined products."))
        self.with_context(context)._generate_serial_numbers()

    @api.onchange('next_serial_qty', 'finished_move_line_ids')
    def _onchange_next_serial_qty(self):
        if self.product_id and self.product_id.tracking == 'lot':
            serial_range = int(int(self.product_uom_qty) / self.next_serial_qty)
            self.next_serial_count = serial_range
            if self.has_tracking == 'lot':
                self.next_serial_count = (self.product_qty - len(self.finished_move_line_ids.ids))

    def _generate_serial_numbers(self, next_serial_count=False, bypass_line_creation=False):
        """ This method will generate `lot_name` from a string (field
        `next_serial`) and create a move line for each generated `lot_name`.
        """
        self.ensure_one()

        if not next_serial_count:
            next_serial_count = self.next_serial_count

        # We look if the serial number contains at least one digit.
        caught_initial_number = regex_findall("\d+", self.next_serial)
        if not caught_initial_number:
            raise UserError(_('The serial number must contain at least one digit.'))
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
        if bypass_line_creation:
            return lot_names
        if not bypass_line_creation:
            move_lines_commands = self._record_mrp_production(lot_names)
        return True

    def produce_predefined_products(self):
        if not self.move_line_component_ids:
            raise ValidationError(_("Please click on Assign Serial Numbers to process with this step."))
        if self.move_line_component_ids and not any(mv.lot_id for mv in self.move_line_component_ids if mv.product_id.tracking != 'none'):
            raise ValidationError(_("Please assign lot to components that will be utilized in manufacturing products."))
        move_raw_ids = self.move_raw_ids.filtered(lambda a: a.product_id and a.product_id.tracking != 'none')
        if move_raw_ids:
            for raw_id in move_raw_ids:
                finished_lot_id = self.move_line_component_ids.mapped('finished_lot_id.id')
                qty_per_material = raw_id.product_uom_qty / self.product_qty
                for lot in finished_lot_id:
                   if qty_per_material != sum(self.move_line_component_ids.filtered(lambda d: d.product_id == raw_id.product_id and d.finished_lot_id.id == lot).mapped('qty_done')):
                        raise ValidationError(_("Please verify the quantity of consumed material products that will be utilized for manufacturing products."))
        context = self._context.copy() or {}
        context.update({'model': 'mrp.production', 'active_id': self.id})
        lot_names = self._generate_serial_numbers(bypass_line_creation=True)
        for lot_name in lot_names:
            ProductProduce = self.env['mrp.product.produce']
            fields = ProductProduce.fields_get()
            default_vals = ProductProduce.with_context({'default_production_id': self.id}).default_get(fields)
            finished_lot_id = self.env['stock.production.lot'].search([
                ('product_id', '=', self.product_id.id), 
                ('company_id', '=', self.company_id.id or self.env.user.company_id.id), 
                ('name', '=', lot_name)])
            if finished_lot_id:
                default_vals.update({'finished_lot_id': finished_lot_id.id})
            if self.has_tracking == 'lot':
                default_vals.update({'qty_producing': self.next_serial_qty})
            elif self.has_tracking == 'serial':
                default_vals.update({'qty_producing': 1})
            product_produce_wizard = self.env['mrp.product.produce'].with_context(
                context).create(default_vals)
            product_produce_wizard.with_context(context)._generate_produce_lines()
            for mv_line in self.move_line_component_ids.filtered(lambda l: l.finished_lot_id == finished_lot_id):
                linked_move = product_produce_wizard.raw_workorder_line_ids.filtered(
                    lambda s: s.move_id == mv_line.move_id and s.product_id == mv_line.product_id)
                if linked_move and linked_move.product_id.tracking != 'none' and mv_line.qty_done == linked_move.qty_done:
                    linked_move.lot_id = mv_line.lot_id.id
            product_produce_wizard.with_context(context).do_produce()

    def _record_mrp_production(self, lot_names):
        if self.is_components_created:
            raise ValidationError(_("You have already created enough components that are required to produce the finished products."))
        context = self._context.copy() or {}
        context.update({'model': 'mrp.production', 'active_id': self.id})
        for lot_name in lot_names:
            ProductProduce = self.env['mrp.product.produce']
            fields = ProductProduce.fields_get()
            default_vals = ProductProduce.with_context({'default_production_id': self.id}).default_get(fields)
            finished_lot_id = self.env['stock.production.lot'].create(
                {'product_id': self.product_id.id, 'company_id': self.company_id.id or self.env.user.company_id.id})
            if self.has_tracking == 'lot':
                default_vals.update({'qty_producing': self.next_serial_qty})
            elif self.has_tracking == 'serial':
                default_vals.update({'qty_producing': 1})
            qty = self.next_serial_qty
            product_produce_wizard = self.env['mrp.product.produce'].with_context(
                    context).create(default_vals)
            for move in self.move_raw_ids:
                qty_to_consume = product_produce_wizard._prepare_component_quantity(move, qty)
                line_values = product_produce_wizard._generate_lines_values(move, qty_to_consume)
                if line_values[0].get('raw_product_produce_id'):
                    line_values[0].pop('raw_product_produce_id', None)
                if line_values[0].get('finished_product_produce_id'):
                    continue
                for line_val in line_values:
                    line_val.update({'production_id': self.id, 'finished_lot_id': finished_lot_id.id})
                self.env['move.line.component'].create(line_values)
        self.is_components_created = True


class MoveLineComponent(models.Model):
    _name = 'move.line.component'
    _inherit = ["mrp.abstract.workorder.line"]
    _order = 'id desc'
    _description = "Predefine Components of Finished Products that will get consumed at time of manufacture"

    production_id = fields.Many2one('mrp.production', 'Manufacturing Order', required=True, check_company=True)
    finished_lot_id = fields.Many2one('stock.production.lot', string='Finished Lot Id')
    total_qty_to_consume = fields.Float(string='Total To Consume', compute='_compute_total_qty_to_consume')

    @api.depends('qty_to_consume')
    def _compute_total_qty_to_consume(self):
        for obj in self:
            obj.total_qty_to_consume = sum(self.search([('production_id', '=', obj.production_id.id), 
                ('product_id', '=', obj.product_id.id)]).mapped('qty_to_consume'))

    def _get_production(self):
        return self.production_id
