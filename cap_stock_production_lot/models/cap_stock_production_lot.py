# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

import logging
from datetime import date, datetime, timedelta
from odoo import api, fields, models, _
from odoo.exceptions import UserError, Warning

_logger = logging.getLogger(__name__)

class ProductionLot(models.Model):

    _inherit = 'stock.production.lot'
    
    

    def base35encode(self, num):
        """Convert from Base10 to Base35."""
        chars = '0123456789ABCDEFGHIJKLMNPQRSTUVWXYZ'
        
        num = abs(num)
        base35 = ''

        while num > 0:
            num, remainder = divmod(num, len(chars))
            base35 = chars[remainder] + base35

        return base35
        
    def base35decode(self, num):
        """Convert from Base35 to Base10"""
        return int(num, 35)
        
    def _set_container_on_ref(self):
        for rec in self:
            num = rec.name[1:]
            base35 = self.base35encode(int(num))
            
            cont = 'D' + base35.zfill(6)
            self.write({
                'ref': cont,
            })
            
    def _generate_lot_name(self, cont):
        for rec in self:
            num = cont[1:]
            base10 = self.base35decode(num)
            
            name = 'C' + str(base10).zfill(10)
            
            return name
            
            
                        
        