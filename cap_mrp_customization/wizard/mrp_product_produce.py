# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class MrpProductProduce(models.TransientModel):
    _inherit = "mrp.product.produce"

    manufacturer_lot = fields.Char(string="Manufacturer's Lot")
    tare_weight = fields.Float(string="Tare Weight")
    gross_weight = fields.Float(string="Gross Weight")
    container_type = fields.Char(string="Container Type")
    manufacture_date = fields.Date(string="Date of Manufacture", default=lambda self: fields.Date.today())
    expiration_date = fields.Date(string="Expiration Date")

    @api.constrains('manufacture_date', 'expiration_date')
    def _check_date(self):
        for line in self:
            if line.manufacture_date and line.expiration_date and \
                    line.expiration_date < line.manufacture_date:
                raise ValidationError(
                    _('The removal date cannot be earlier than the manufacture date.'))


    def do_produce(self):
        if self.finished_lot_id:
            self.finished_lot_id.manufacturer_lot = self.manufacturer_lot
            self.finished_lot_id.tare_weight = self.tare_weight
            self.finished_lot_id.gross_weight = self.gross_weight
            self.finished_lot_id.container_type = self.container_type
            self.finished_lot_id.manufacture_date = self.manufacture_date
            self.finished_lot_id.removal_date = self.expiration_date
        return super(MrpProductProduce, self).do_produce()