# -*- coding: utf-8 -*-

from odoo import api, models, fields, _
from odoo.exceptions import ValidationError


class StockProductionLot(models.Model):
    _inherit = 'stock.production.lot'

    manufacturer_lot = fields.Char(string="Manufacturer's Lot")
    tare_weight = fields.Float(string="Tare Weight")
    gross_weight = fields.Float(string="Gross Weight")
    container_type = fields.Char(string="Container Type")
    manufacture_date = fields.Date(string="Date of Manufacture")

    @api.constrains('manufacture_date', 'removal_date')
    def _check_date(self):
        for line in self:
            if line.manufacture_date and line.removal_date and \
                    line.removal_date.date() < line.manufacture_date:
                raise ValidationError(
                    _('The removal date cannot be earlier than the manufacture date.'))

