# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class Picking(models.Model):
    _inherit = "stock.picking"

    def button_validate(self):
        for move_line in self.move_line_nosuggest_ids:
            if move_line.lot_id:
                move_line.lot_id.removal_date = move_line.expiration_date
                move_line.lot_id.manufacturer_lot = move_line.manufacturer_lot
        return super(Picking, self).button_validate()