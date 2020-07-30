# -*- coding: utf-8 -*-

from odoo import api, models, fields, _
from odoo.exceptions import ValidationError
from odoo.osv import expression


class StockProductionLot(models.Model):
    _inherit = 'stock.production.lot'

    manufacturer_lot = fields.Char(string="Manufacturer's Lot")
    supplier_lot = fields.Char(string="Supplier's Lot")
    supplier_id = fields.Many2one('res.partner', string="Supplier")
    tare_weight = fields.Float(string="Tare Weight")
    gross_weight = fields.Float(string="Gross Weight")
    component_weight = fields.Float(string="Component Weight")
    container_type = fields.Selection([('1 GAL', '1 GAL'), ('4x1 BOX', '4x1 BOX'), ('BAG', 'BAG'), 
        ('BOTTLE', 'BOTTLE'), ('BOTTLE-2.5', 'BOTTLE-2.5'), ('BOX', 'BOX'), ('DELTANG-5', 'DELTANG-5'), 
        ('DRUM', 'DRUM'), ('DRUM-55', 'DRUM-55'), ('DRUM-FIBER', 'DRUM-FIBER'), ('CB500', 'CB500'), 
        ('CB1000', 'CB1000'), ('LABEL', 'LABEL'), ('NA', 'NA'), ('PAIL', 'PAIL'), ('PAIL-5', 'PAIL-5'), 
        ('PALLET', 'PALLET'), ('TANKER', 'TANKER'), ('TOTE', 'TOTE'), ('TRAY', 'TRAY')], string="Container Type")
    manufacture_date = fields.Date(string="Date of Manufacture")

    @api.constrains('manufacture_date', 'removal_date')
    def _check_date(self):
        for line in self:
            if line.manufacture_date and line.removal_date and \
                    line.removal_date.date() < line.manufacture_date:
                raise ValidationError(
                    _('The removal date cannot be earlier than the manufacture date.'))

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        context = self._context.copy() or {}
        if context.get('filter_lot_details'):
            total_qty_to_consume = context.get('total_qty_to_consume') or context.get('product_uom_qty')
            lots_id = []
            domain = []
            lot_ids = self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)
            if lot_ids and total_qty_to_consume:
                for lot in self.browse(lot_ids):
                    if lot.product_qty > total_qty_to_consume:
                        lots_id.append(lot.id)
            domain.append(('id', 'in', lots_id))
            lot_ids = self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)
            return models.lazy_name_get(self.browse(lot_ids).with_user(name_get_uid))
        elif context.get('from_product'):
            product_id = context.get('default_product_id')
            company_id = context.get('default_company_id')
            lot_ids = self.search([('product_id', '=', product_id), ('company_id', '=', company_id), 
                ('name', 'ilike', name)]).ids
            return models.lazy_name_get(self.browse(lot_ids).with_user(name_get_uid))
        return super(StockProductionLot, self)._name_search(name, args, operator, limit, name_get_uid)