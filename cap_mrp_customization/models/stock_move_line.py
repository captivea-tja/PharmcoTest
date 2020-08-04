# -*- coding: utf-8 -*-
from odoo import api, models, fields, _
from odoo.exceptions import ValidationError


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    manufacturer_lot = fields.Char(string="Manufacturer's Lot")
    expiration_date = fields.Date(string="Expiration Date")
    supplier_lot = fields.Char(string="Supplier's Lot")
    supplier_id = fields.Many2one('res.partner', string="Supplier")
    tare_weight = fields.Float(string="Tare Weight")
    component_weight = fields.Float(string="Gross Weight")
    gross_weight = fields.Float(string="Gross Weight")
    container_type = fields.Selection([('1 GAL', '1 GAL'), ('4x1 BOX', '4x1 BOX'), ('BAG', 'BAG'),
        ('BOTTLE', 'BOTTLE'), ('BOTTLE-2.5', 'BOTTLE-2.5'), ('BOX', 'BOX'), ('DELTANG-5', 'DELTANG-5'),
        ('DRUM', 'DRUM'), ('DRUM-55', 'DRUM-55'), ('DRUM-FIBER', 'DRUM-FIBER'), ('CB500', 'CB500'),
        ('CB1000', 'CB1000'), ('LABEL', 'LABEL'), ('NA', 'NA'), ('PAIL', 'PAIL'), ('PAIL-5', 'PAIL-5'),
        ('PALLET', 'PALLET'), ('TANKER', 'TANKER'), ('TOTE', 'TOTE'), ('TRAY', 'TRAY')], string="Container Type")
    manufacture_date = fields.Date(string="Date of Manufacture")
    ref = fields.Char('Container Code', related='lot_id.ref',
        help="Internal reference number in case it differs from the manufacturer's lot/serial number")

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
                'supplier_lot': move_id.supplier_lot,
                'supplier_id': move_id.supplier_id.id,
                'expiration_date': move_id.expiration_date,
                'tare_weight': move_id.tare_weight,
                'component_weight': move_id.component_weight,
                'gross_weight': move_id.gross_weight,
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