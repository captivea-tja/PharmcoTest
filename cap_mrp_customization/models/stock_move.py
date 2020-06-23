# -*- coding: utf-8 -*-

from odoo import api, models, fields, _


class StockMove(models.Model):
    _inherit = 'stock.move'

    def action_show_details(self):
        res = super(StockMove, self).action_show_details()
        res.update({'target': self})
        return res
