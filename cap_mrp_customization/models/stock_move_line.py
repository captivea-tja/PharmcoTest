# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models, fields


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    manufacturer_lot = fields.Char(string="Manufacturer's Lot")
    expiration_date = fields.Date(string="Expiration Date")
