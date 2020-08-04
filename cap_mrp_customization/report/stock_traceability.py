# -*- coding: utf-8 -*-
from odoo import api, models
from odoo.addons.stock.report.stock_traceability import autoIncrement


class MrpStockReport(models.TransientModel):
    _inherit = 'stock.traceability.report'

    @api.model
    def _final_vals_to_lines(self, final_vals, level):
        lines = []
        for data in final_vals:
            # Added an extra column for manufacturer's lot on traceability report
            manufacturer_lot = ''
            ref = ''
            if data.get('lot_id', False):
                manufacturer_lot = self.env['stock.production.lot'].browse(
                    data.get('lot_id', False)).mapped('manufacturer_lot')
                manufacturer_lot = manufacturer_lot and manufacturer_lot[0]
                ref = self.env['stock.production.lot'].browse(
                    data.get('lot_id', False)).mapped('ref')
                ref = ref and ref[0]
            lines.append({
                'id': autoIncrement(),
                'model': data['model'],
                'model_id': data['model_id'],
                'parent_id': data['parent_id'],
                'usage': data.get('usage', False),
                'is_used': data.get('is_used', False),
                'lot_name': data.get('lot_name', False),
                'lot_id': data.get('lot_id', False),
                'manufacturer_lot': manufacturer_lot or '',
                'reference': data.get('reference_id', False),
                'res_id': data.get('res_id', False),
                'res_model': data.get('res_model', False),
                'columns': [data.get('reference_id', False),
                            data.get('product_id', False),
                            data.get('date', False),
                            data.get('lot_name', False),
                            ref or '',
                            manufacturer_lot or '',
                            data.get('location_source', False),
                            data.get('location_destination', False),
                            data.get('product_qty_uom', 0)],
                'level': level,
                'unfoldable': data['unfoldable'],
            })
        return lines

    @api.model
    def get_lines(self, line_id=None, **kw):
        context = dict(self.env.context)
        model = kw and kw['model_name'] or context.get('model')
        rec_id = kw and kw['model_id'] or context.get('active_id')
        level = kw and kw['level'] or 1
        lines = self.env['stock.move.line']
        move_line = self.env['stock.move.line']
        if rec_id and model == 'stock.production.lot':
            lines = move_line.search([
                ('lot_id', '=', context.get('lot_name') or rec_id),
                ('state', '=', 'done'),
            ])
        elif  rec_id and model == 'stock.move.line' and context.get('lot_name'):
            record = self.env[model].browse(rec_id)
            dummy, is_used = self._get_linked_move_lines(record)
            if is_used:
                lines = is_used
        elif rec_id and model in ('stock.picking', 'mrp.production'):
            record = self.env[model].browse(rec_id)
            if model == 'stock.picking':
                lines = record.move_lines.mapped('move_line_ids').filtered(lambda m: m.lot_id and m.state == 'done')
            else:
                lines = record.move_finished_ids.mapped('move_line_ids').filtered(lambda m: m.state == 'done')
        
        # Added extra condition to get trailing move lines when lots are splited from Inventory Adjustment.
        if rec_id and model == 'stock.production.lot':
            for line in lines:
                if line.move_id.inventory_id.move_ids:
                    stock_move_lines = self.env['stock.move.line'].search([('move_id', '=', line.move_id.inventory_id.move_ids.ids)])
                    lines |= stock_move_lines

        move_line_vals = self._lines(line_id, model_id=rec_id, model=model, level=level, move_lines=lines)
        final_vals = sorted(move_line_vals, key=lambda v: v['date'], reverse=True)
        lines = self._final_vals_to_lines(final_vals, level)
        return lines