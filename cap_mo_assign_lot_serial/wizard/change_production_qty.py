# -*- coding: utf-8 -*-

from odoo import models, _
from odoo.exceptions import ValidationError

class ChangeProductionQty(models.TransientModel):
    _inherit = "change.production.qty"

    def change_prod_qty(self):
        super(ChangeProductionQty, self).change_prod_qty()
        if self.mo_id:
        	self.mo_id.next_serial = self.mo_id.product_qty
        	self.mo_id.is_components_created = False
        	self.mo_id.move_line_component_ids.unlink()