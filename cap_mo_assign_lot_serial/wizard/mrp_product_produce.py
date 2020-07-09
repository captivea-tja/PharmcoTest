# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class MrpProductProduce(models.TransientModel):
    _inherit = "mrp.product.produce"

    # OVerwritten to create lines on MO to add serial and lots
    def _generate_produce_lines(self):
        """ When the wizard is called in backend, the onchange that create the
        produce lines is not trigger. This method generate them and is used with
        _record_production to appropriately set the lot_produced_id and
        appropriately create raw stock move lines.
        """
        self.ensure_one()
        moves = (self.move_raw_ids | self.move_finished_ids).filtered(
            lambda move: move.state not in ('done', 'cancel')
        )
        for move in moves:
            qty_to_consume = self._prepare_component_quantity(move, self.qty_producing)
            line_values = self._generate_lines_values(move, qty_to_consume)
            self.env['mrp.product.produce.line'].create(line_values)
            if line_values[0].get('raw_product_produce_id'):
                line_values[0].pop('raw_product_produce_id', None)
            if line_values[0].get('finished_product_produce_id'):
                continue
                # line_values[0].pop('finished_product_produce_id', None)
            for line_val in line_values:
                line_val.update({'production_id': self.production_id.id})
            if self.production_id and self.production_id.move_raw_ids:
                products = self.production_id.move_raw_ids.mapped('product_id.id')
