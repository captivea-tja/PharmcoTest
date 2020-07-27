# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class MrpProduction(models.Model):
    """ Manufacturing Orders """
    _inherit = 'mrp.production'

    manufacturer_lot = fields.Char(string="Manufacturer's Lot")
    tare_weight = fields.Float(string="Tare Weight")
    gross_weight = fields.Float(string="Gross Weight", compute="_compute_gross_weight")
    component_weight = fields.Float(string="Component Weight", compute="_compute_component_weight")
    container_type = fields.Selection([('1 GAL', '1 GAL'), ('4x1 BOX', '4x1 BOX'), ('BAG', 'BAG'),
        ('BOTTLE', 'BOTTLE'), ('BOTTLE-2.5', 'BOTTLE-2.5'), ('BOX', 'BOX'), ('DELTANG-5', 'DELTANG-5'),
        ('DRUM', 'DRUM'), ('DRUM-55', 'DRUM-55'), ('DRUM-FIBER', 'DRUM-FIBER'), ('CB500', 'CB500'),
        ('CB1000', 'CB1000'), ('LABEL', 'LABEL'), ('NA', 'NA'), ('PAIL', 'PAIL'), ('PAIL-5', 'PAIL-5'),
        ('PALLET', 'PALLET'), ('TANKER', 'TANKER'), ('TOTE', 'TOTE'), ('TRAY', 'TRAY')], string="Container Type")
    manufacture_date = fields.Date(string="Date of Manufacture", default=lambda self: fields.Date.today())
    # expiration_date = fields.Date(string="Expiration Date")

    @api.depends('tare_weight', 'product_qty', 'move_raw_ids')
    def _compute_gross_weight(self):
        for line in self:
            gross_weight = 0
            if line.has_tracking == 'lot':
                gross_weight = line.product_qty + line.tare_weight
            if line.has_tracking == 'serial':
                gross_weight = line.component_weight + line.tare_weight
            line.gross_weight = gross_weight

    @api.depends('move_raw_ids', 'state')
    def _compute_component_weight(self):
        for line in self:
            total = 0
            if line.has_tracking == 'serial':
                for component in line.move_raw_ids:
                    if component.product_uom.name == 'kg':
                        total += component.product_uom_qty
            line.component_weight = total

    # @api.constrains('manufacture_date', 'expiration_date')
    # def _check_date(self):
    #     for line in self:
    #         if line.manufacture_date and line.expiration_date and \
    #                 line.expiration_date < line.manufacture_date:
    #             raise ValidationError(
    #                 _('The removal date cannot be earlier than the manufacture date.'))


class MoveLineComponent(models.Model):
    _inherit = 'move.line.component'

    @api.model
    def create(self, vals):
        if vals.get('move_id'):
            move_lot_id = self.env['stock.move'].search([('id', '=', vals.get('move_id'))]).lot_id.id
            product_tracking = self.env['product.product'].search([('id', '=', vals.get('product_id'))]).tracking
            if move_lot_id and product_tracking == 'lot':
                vals.update({'lot_id': move_lot_id})
        return super(MoveLineComponent, self).create(vals)
