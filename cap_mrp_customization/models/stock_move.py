# -*- coding: utf-8 -*-

from odoo import api, models, fields, _


class StockMove(models.Model):
    _inherit = 'stock.move'

    manufacturer_lot = fields.Char(string="Manufacturer's Lot")
    expiration_date = fields.Date(string="Expiration Date")
    tare_weight = fields.Float(string="Tare Weight")
    container_type = fields.Char(string="Container Type")
    manufacture_date = fields.Date(string="Date of Manufacture")

    def generate_sequence_number(self):
        sequence_ref = self.env.ref('stock.sequence_production_lots')
        if sequence_ref and sequence_ref.number_next_actual:
            next_seq = sequence_ref.get_next_char(sequence_ref.number_next_actual)
            self.next_serial = next_seq

    def action_show_details(self):
        res = super(StockMove, self).action_show_details()
        res.update({'target': self})
        return res
