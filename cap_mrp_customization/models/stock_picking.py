# -*- coding: utf-8 -*-

from odoo import api, fields, models


class Picking(models.Model):
    _inherit = "stock.picking"

    def button_validate(self):
        for move_line in self.move_line_nosuggest_ids:
            if move_line.lot_id:
                move_line.lot_id.removal_date = move_line.expiration_date
                move_line.lot_id.manufacturer_lot = move_line.manufacturer_lot
                move_line.lot_id.tare_weight = move_line.tare_weight
                move_line.lot_id.gross_weight = move_line.gross_weight
                move_line.lot_id.container_type = move_line.container_type
                move_line.lot_id.manufacture_date = move_line.manufacture_date
        return super(Picking, self).button_validate()