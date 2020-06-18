# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models, fields


class StockProductionLot(models.Model):
    _inherit = 'stock.production.lot'

    manufacturer_lot = fields.Char(string="Manufacturer's Lot")
