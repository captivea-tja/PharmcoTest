# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class MrpProductProduce(models.TransientModel):
    _inherit = "mrp.product.produce"

    @api.depends('tare_weight', 'qty_producing')
    def _compute_gross_weight(self):
        for line in self:
            line.gross_weight = line.qty_producing + line.tare_weight

    def do_produce(self):
        if self.finished_lot_id and self.production_id:
            self.finished_lot_id.manufacturer_lot = self.production_id.manufacturer_lot
            self.finished_lot_id.tare_weight = self.production_id.tare_weight
            self.finished_lot_id.gross_weight = self.production_id.gross_weight
            self.finished_lot_id.container_type = self.production_id.container_type
            self.finished_lot_id.manufacture_date = self.production_id.manufacture_date
            # self.finished_lot_id.removal_date = self.production_id.expiration_date
        return super(MrpProductProduce, self).do_produce()

    def continue_production(self):
        if self.finished_lot_id and self.production_id:
            self.finished_lot_id.manufacturer_lot = self.production_id.manufacturer_lot
            self.finished_lot_id.tare_weight = self.production_id.tare_weight
            self.finished_lot_id.gross_weight = self.production_id.gross_weight
            self.finished_lot_id.container_type = self.production_id.container_type
            self.finished_lot_id.manufacture_date = self.production_id.manufacture_date
            # self.finished_lot_id.removal_date = self.production_id.expiration_date
        return super(MrpProductProduce, self).continue_production()
