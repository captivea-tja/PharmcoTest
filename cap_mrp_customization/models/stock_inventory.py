# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class InventoryLine(models.Model):
    _inherit = "stock.inventory.line"

    ref_lot_id = fields.Many2one(
        'stock.production.lot', 'Reference Lot/Serial Number', check_company=True,
        domain="[('product_id','=',product_id), ('company_id', '=', company_id)]",
        help="Adds default Manufacturer's Lot and Removal date from this lot")
    

class Inventory(models.Model):
    _inherit = "stock.inventory"

    def action_validate(self):
        inventory_lines = self.line_ids.filtered(
            lambda l: l.product_id.tracking in ['lot', 'serial'] and \
            l.prod_lot_id and l.ref_lot_id and l.theoretical_qty != l.product_qty)
        if inventory_lines:
            for line in inventory_lines:
                if line.ref_lot_id:
                    line.prod_lot_id.removal_date = line.ref_lot_id.removal_date
                    line.prod_lot_id.manufacturer_lot = line.ref_lot_id.manufacturer_lot
        return super(Inventory, self).action_validate()
        