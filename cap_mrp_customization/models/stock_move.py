# -*- coding: utf-8 -*-

from odoo import api, models, fields, _


class StockMove(models.Model):
    _inherit = 'stock.move'

    manufacturer_lot = fields.Char(string="Manufacturer's Lot")
    supplier_lot = fields.Char(string="Supplier's Lot")
    supplier_id = fields.Many2one('res.partner', string="Supplier")
    expiration_date = fields.Date(string="Expiration Date")
    tare_weight = fields.Float(string="Tare Weight")
    gross_weight = fields.Float(string="Gross Weight")
    container_type = fields.Selection([('1 GAL', '1 GAL'), ('4x1 BOX', '4x1 BOX'), ('BAG', 'BAG'),
        ('BOTTLE', 'BOTTLE'), ('BOTTLE-2.5', 'BOTTLE-2.5'), ('BOX', 'BOX'), ('DELTANG-5', 'DELTANG-5'),
        ('DRUM', 'DRUM'), ('DRUM-55', 'DRUM-55'), ('DRUM-FIBER', 'DRUM-FIBER'), ('CB500', 'CB500'),
        ('CB1000', 'CB1000'), ('LABEL', 'LABEL'), ('NA', 'NA'), ('PAIL', 'PAIL'), ('PAIL-5', 'PAIL-5'),
        ('PALLET', 'PALLET'), ('TANKER', 'TANKER'), ('TOTE', 'TOTE'), ('TRAY', 'TRAY')], string="Container Type")
    manufacture_date = fields.Date(string="Date of Manufacture")
    lot_id = fields.Many2one('stock.production.lot', string="Lot to consume")

    def generate_sequence_number(self):
        sequence_ref = self.env.ref('stock.sequence_production_lots')
        if sequence_ref and sequence_ref.number_next_actual:
            next_seq = sequence_ref.get_next_char(sequence_ref.number_next_actual)
            self.next_serial = next_seq

    def action_show_details(self):
        res = super(StockMove, self).action_show_details()
        res.update({'target': self})
        return res
