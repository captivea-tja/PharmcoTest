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
                move_line.lot_id.container_type = move_line.container_type
                move_line.lot_id.manufacture_date = move_line.manufacture_date
                move_line.lot_id.supplier_lot = move_line.supplier_lot
                move_line.lot_id.supplier_id = move_line.supplier_id.id
        return super(Picking, self).button_validate()

    def _create_backorder(self):
        res = super(Picking, self)._create_backorder()
        for order in res:
            move_ids = self.env['stock.move'].browse(order.move_ids_without_package.ids)
            for move in move_ids:
                move.next_serial = False
                move.next_serial_qty = False
                move.next_serial_count = False
                move.manufacture_date = False
                move.tare_weight = False
                move.container_type = False
                move.manufacturer_lot = False
                move.expiration_date = False
                move.supplier_lot = False
                move.supplier_id = False
        return res