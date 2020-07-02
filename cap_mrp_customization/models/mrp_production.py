# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class MrpProduction(models.Model):
    """ Manufacturing Orders """
    _inherit = 'mrp.production'

    manufacturer_lot = fields.Char(string="Manufacturer's Lot")
    tare_weight = fields.Float(string="Tare Weight")
    gross_weight = fields.Float(string="Gross Weight", compute="_compute_gross_weight")
    container_type = fields.Char(string="Container Type")
    manufacture_date = fields.Date(string="Date of Manufacture", default=lambda self: fields.Date.today())
    expiration_date = fields.Date(string="Expiration Date")

    @api.depends('tare_weight', 'product_qty')
    def _compute_gross_weight(self):
        for line in self:
            line.gross_weight = line.product_qty + line.tare_weight

    def open_produce_product(self):
        res = super(MrpProduction, self).open_produce_product()
        if res:
            context = res.get('context') or {}
            if isinstance(context, str) and context == '{}':
                context = {}
            context.update({
                'default_manufacturer_lot': self.manufacturer_lot or '',
                'default_tare_weight': self.tare_weight or '',
                'default_container_type': self.container_type or '',
                'default_manufacture_date': self.manufacture_date or '',
                'default_expiration_date': self.expiration_date or '',
            })
            res.update({'context': context})
        return res