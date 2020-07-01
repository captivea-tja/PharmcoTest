# -*- coding: utf-8 -*-
from odoo import api, models, fields, _
from odoo.exceptions import ValidationError


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    manufacturer_lot = fields.Char(string="Manufacturer's Lot")
    expiration_date = fields.Date(string="Expiration Date")
    tare_weight = fields.Float(string="Tare Weight")
    gross_weight = fields.Float(string="Gross Weight", compute="_compute_gross_weight")
    container_type = fields.Char(string="Container Type")
    manufacture_date = fields.Date(string="Date of Manufacture")

    @api.depends('tare_weight', 'qty_done')
    def _compute_gross_weight(self):
        for line in self:
            line.gross_weight = line.qty_done + line.tare_weight

    @api.constrains('manufacture_date', 'expiration_date')
    def _check_date(self):
        for line in self:
            if line.manufacture_date and line.expiration_date and \
                    line.expiration_date < line.manufacture_date:
                raise ValidationError(
                    _('The expiration date cannot be earlier than the manufacture date.'))

    def action_generate_serial(self):
        self.ensure_one()
        product_produce_wiz = self.env.ref('stock.view_move_line_form', False)
        self.lot_id = self.env['stock.production.lot'].create({
            'product_id': self.product_id.id,
            'company_id': self.company_id.id
        })

    @api.model
    def create(self, vals):
        if vals.get('move_id'):
            move_id = self.env['stock.move'].browse(vals.get('move_id'))
            vals.update({
                'manufacturer_lot': move_id.manufacturer_lot,
                'expiration_date': move_id.expiration_date,
                'tare_weight': move_id.tare_weight,
                'container_type': move_id.container_type,
                'manufacture_date': move_id.manufacture_date
            })
        if not vals.get('lot_id', False) and vals.get('lot_name', False):
            lot_id = self.env['stock.production.lot'].create({
                'product_id': vals.get('product_id'),
                'company_id': vals.get('company_id') or self.env.user.company_id.id
            })
            vals.update({'lot_id': lot_id.id})
        return super(StockMoveLine, self).create(vals)