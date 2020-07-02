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
        context = self._context or {}
        mrp_id = False
        if context and context.get('params') and context['params'].get('model') == 'mrp.production':
            mrp_id = self.env['mrp.production'].browse(context['params'].get('id'))
        if self.finished_lot_id and mrp_id:
            self.finished_lot_id.manufacturer_lot = mrp_id.manufacturer_lot
            self.finished_lot_id.tare_weight = mrp_id.tare_weight
            self.finished_lot_id.gross_weight = mrp_id.gross_weight
            self.finished_lot_id.container_type = mrp_id.container_type
            self.finished_lot_id.manufacture_date = mrp_id.manufacture_date
            self.finished_lot_id.removal_date = mrp_id.expiration_date
        return super(MrpProductProduce, self).do_produce()

    def continue_production(self):
        context = self._context or {}
        mrp_id = False
        if context and context.get('params') and context['params'].get('model') == 'mrp.production':
            mrp_id = self.env['mrp.production'].browse(context['params'].get('id'))
        if self.finished_lot_id and mrp_id:
            self.finished_lot_id.manufacturer_lot = mrp_id.manufacturer_lot
            self.finished_lot_id.tare_weight = mrp_id.tare_weight
            self.finished_lot_id.gross_weight = mrp_id.gross_weight
            self.finished_lot_id.container_type = mrp_id.container_type
            self.finished_lot_id.manufacture_date = mrp_id.manufacture_date
            self.finished_lot_id.removal_date = mrp_id.expiration_date
        return super(MrpProductProduce, self).continue_production()