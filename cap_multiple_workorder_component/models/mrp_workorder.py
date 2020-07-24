from odoo import api, fields, models, _
from odoo.tools import float_compare, float_round
from odoo.exceptions import UserError



class MrpProductionWorkcenterLine(models.Model):
    _inherit = 'mrp.workorder'

    current_quality_check_id_2 = fields.Many2one(
        'quality.check', "Current Quality Check", store=True, check_company=True)
    component_id_2 = fields.Many2one('product.product', related='current_quality_check_id_2.component_id')
    component_tracking_2 = fields.Selection(related='component_id_2.tracking', string="Is Component Tracked", readonly=False)
    component_remaining_qty_2 = fields.Float('Remaining Quantity for Component', compute='_compute_component_data', digits='Product Unit of Measure')
    component_uom_id_2 = fields.Many2one('uom.uom', compute='_compute_component_data', string="Component UoM")
    control_date_2 = fields.Datetime(related='current_quality_check_id_2.control_date', readonly=False)
    lot_id_2 = fields.Many2one(related='current_quality_check_id_2.lot_id', readonly=False)
    workorder_line_id_2 = fields.Many2one(related='current_quality_check_id_2.workorder_line_id', readonly=False)
    note_2 = fields.Html(related='current_quality_check_id_2.note')
    quality_state_2 = fields.Selection(related='current_quality_check_id_2.quality_state', string="Quality State", readonly=False)
    qty_done_2 = fields.Float(related='current_quality_check_id_2.qty_done', readonly=False)
    test_type_2_id = fields.Many2one('quality.point.test_type', 'Test Type', related='current_quality_check_id_2.test_type_id')
    user_id_2 = fields.Many2one(related='current_quality_check_id_2.user_id', readonly=False)
    picture_2 = fields.Binary(related='current_quality_check_id_2.picture', readonly=False)
    measure_2 = fields.Float(related='current_quality_check_id_2.measure', readonly=False)
    measure_success_2 = fields.Selection(related='current_quality_check_id_2.measure_success', readonly=False)
    norm_unit_2 = fields.Char(related='current_quality_check_id_2.norm_unit', readonly=False)

    def _compute_component_data(self):
        '''
        Overwritten this function to manage multiple components to proceed with the consumption on same order.
        '''
        res = super(MrpProductionWorkcenterLine, self)._change_quality_check()
        self.component_remaining_qty_2 = False
        self.component_uom_id_2 = False
        self.component_remaining_qty = False
        self.component_uom_id = False
        for wo in self.filtered(lambda w: w.state not in ('done', 'cancel')):
            if wo.test_type in ('register_byproducts', 'register_consumed_materials') and wo.quality_state == 'none':
                move = wo.current_quality_check_id.workorder_line_id.move_id
                lines = wo._workorder_line_ids().filtered(lambda l: l.move_id == move)
                completed_lines = lines.filtered(lambda l: l.lot_id) if wo.component_id.tracking != 'none' else lines
                wo.component_remaining_qty = self._prepare_component_quantity(move, wo.qty_producing) - sum(completed_lines.mapped('qty_done'))
                wo.component_uom_id = lines[:1].product_uom_id
                move_2 = wo.current_quality_check_id_2.workorder_line_id.move_id
                lines_2 = wo._workorder_line_ids().filtered(lambda l: l.move_id == move_2)
                completed_lines_2 = lines_2.filtered(lambda l: l.lot_id) if wo.component_id_2.tracking != 'none' else lines_2
                wo.component_remaining_qty_2 = self._prepare_component_quantity(move_2, wo.qty_producing) - sum(completed_lines_2.mapped('qty_done'))
                wo.component_uom_id_2 = lines[:1].product_uom_id
        return res

    def _change_quality_check(self, **params):
        """
        Inherited this function to manage other components to proceed with the consumption on same order.
        """

        self.ensure_one()
        res = super(MrpProductionWorkcenterLine, self)._change_quality_check()
        
        check_id_2 = None
        # Determine the list of checks to consider
        checks = params['checks'] if 'checks' in params else self.check_ids
        if not params.get('children'):
            checks = checks.filtered(lambda c: not c.parent_id)
        # We need to make sure the current quality check is in our list
        # when we compute position relatively to the current quality check.
        if 'increment' in params or 'checks' in params and self.current_quality_check_id_2 not in checks:
            checks |= self.current_quality_check_id_2
        # Restrict to checks associated with the current production
        checks = checks.filtered(lambda c: c.finished_product_sequence == self.qty_produced)
        # As some checks are generated on the fly,
        # we need to ensure that all 'children' steps are grouped together.
        # Missing steps are added at the end.
        def sort_quality_checks(check):
            # Useful tuples to compute the order
            parent_point_sequence = (check.parent_id.point_id.sequence, check.parent_id.point_id.id)
            point_sequence = (check.point_id.sequence, check.point_id.id)
            # Parent quality checks are sorted according to the sequence number of their associated quality point,
            # with chronological order being the tie-breaker.
            if check.point_id and not check.parent_id:
                score = (0, 0) + point_sequence + (0, 0)
            # Children steps follow their parents, honouring their quality point sequence number,
            # with chronological order being the tie-breaker.
            elif check.point_id:
                score = (0, 0) + parent_point_sequence + point_sequence
            # Checks without points go at the end and are ordered chronologically
            elif not check.parent_id:
                score = (check.id, 0, 0, 0, 0, 0)
            # Children without points follow their respective parents, in chronological order
            else:
                score = (check.parent_id.id, check.id, 0, 0, 0, 0)
            return score

        ordered_check_ids = checks.sorted(key=sort_quality_checks).ids
        # We manually add a final 'Summary' step
        # which is not associated with a specific quality_check (hence the 'False' id).
        ordered_check_ids.append(False)
        # order_check_len = len(ordered_check_ids) - 1
        order_check_len = len(ordered_check_ids)
        # Determine the quality check we are switching to

        if 'increment' in params:
            increment = params.get('increment')
            from_last_step = not self.current_quality_check_id and not self.current_quality_check_id_2
            
            even = False
            if (order_check_len % 2) == 0:
                even = True

            if from_last_step and increment < 0:
                if not even:
                    order_check_len -= 1
                    increment -= 1

            current_id = self.current_quality_check_id.id
            if current_id:
                if increment > 0:
                    increment += 1
                elif increment < 0:
                    increment -= 1

            position = ordered_check_ids.index(current_id)
            position = position + increment
            if position in range(0, order_check_len):
                check_id = ordered_check_ids[position]
            else:
                check_id = False
            
            current_id_2 = self.current_quality_check_id_2.id
            position_2 = ordered_check_ids.index(current_id_2)
            if from_last_step and params.get('increment') < 0:
                if not even:
                    position_2 = position_2 + params.get('increment')
            else:
                position_2 = position_2 + increment
            
            if position_2 in range(0, order_check_len):
                if check_id != ordered_check_ids[position_2]:
                    check_id_2 = ordered_check_ids[position_2]
                else:
                    check_id_2 = False
            else: 
                check_id_2 = False
        elif params.get('position') in range(0, order_check_len):
            position = params['position']
            check_id = ordered_check_ids[position]
            position_2 = position
            if position < 0:
                position_2 -= 1
            if position >= 0:
                position_2 += 1
            if position_2 in range(0, order_check_len):
                if check_id != ordered_check_ids[position_2]:
                    check_id_2 = ordered_check_ids[position_2]
                else:
                    check_id_2 = False
            else: 
                check_id_2 = False
        elif params.get('goto') in ordered_check_ids:
            check_id = params['goto']
            position = ordered_check_ids.index(check_id)

            position_2 = position + 1
            if position_2 in range(0, order_check_len):
                check_id_2 = ordered_check_ids[position + 1]
            else: 
                check_id_2 = False
        
        # Change the quality check and the worksheet page if necessary
        if check_id_2 is not None:
            next_check_2 = self.env['quality.check'].browse(check_id_2)
            change_worksheet_page = position_2 != order_check_len and next_check_2.point_id.worksheet == 'scroll'
            checks = self.check_ids.filtered(lambda c: c.finished_product_sequence == self.qty_produced)
            curr_pos = params.get('position') and params.get('position') + 1
            vals = {
                'allow_producing_quantity_change': True if curr_pos == 0 and all(c.quality_state == 'none' for c in checks) else False,
                'current_quality_check_id': check_id,
                'current_quality_check_id_2': check_id_2,
                'is_first_step': position == 0 or position_2 == 0,
                'is_last_step': check_id == False and check_id_2 == False,
                'worksheet_page': next_check_2.point_id.worksheet_page if change_worksheet_page else self.worksheet_page,
            }
            self.write({
                'allow_producing_quantity_change': True if curr_pos == 0 and all(c.quality_state == 'none' for c in checks) else False,
                'current_quality_check_id': check_id,
                'current_quality_check_id_2': check_id_2,
                'is_first_step': position == 0 or position_2 == 0,
                'is_last_step': check_id == False and check_id_2 == False,
                'worksheet_page': next_check_2.point_id.worksheet_page if change_worksheet_page else self.worksheet_page,
            })
        return res

    def _next(self, continue_production=False):
        """ This function:
        - first: fullfill related move line with right lot and validated quantity.
        - second: Generate new quality check for remaining quantity and link them to the original check.
        - third: Pass to the next check or return a failure message.

        # Inherited this function to manage other components to proceed with the consumption on same order.
        Overwritten this function to manage multiple components to proceed with the consumption on same order.
        """
        
        self.ensure_one()
        rounding = self.product_uom_id.rounding
        workorder_line_id_2 = self.current_quality_check_id_2.workorder_line_id
        if float_compare(self.qty_producing, 0, precision_rounding=rounding) <= 0\
                or float_compare(self.qty_producing, self.qty_remaining, precision_rounding=rounding) > 0:
            raise UserError(_('Please ensure the quantity to produce is nonnegative and does not exceed the remaining quantity.'))
        elif self.test_type in ('register_byproducts', 'register_consumed_materials'):
            # Form validation
            # in case we use continue production instead of validate button.
            # We would like to consume 0 and leave lot_id blank to close the consumption
            if self.component_tracking != 'none' and not self.lot_id and self.qty_done != 0:
                raise UserError(_('Please enter a Lot/SN.'))
            if self.component_tracking_2 != 'none' and not self.lot_id_2 and self.qty_done_2 != 0:
                raise UserError(_('Please enter a Lot/SN.'))
            if float_compare(self.qty_done, 0, precision_rounding=rounding) < 0:
                raise UserError(_('Please enter a positive quantity.'))
            if float_compare(self.qty_done_2, 0, precision_rounding=rounding) < 0:
                raise UserError(_('Please enter a positive quantity.'))

            # Get the move lines associated with our component
            self.component_remaining_qty -= float_round(self.qty_done, precision_rounding=self.workorder_line_id.product_uom_id.rounding or rounding)
            self.component_remaining_qty_2 -= float_round(self.qty_done_2, precision_rounding=workorder_line_id_2.product_uom_id.rounding or rounding)
            # Write the lot and qty to the move line
            self.workorder_line_id.write({'lot_id': self.lot_id.id, 'qty_done': float_round(self.qty_done, precision_rounding=self.workorder_line_id.product_uom_id.rounding or rounding)})
            workorder_line_id_2.write({'lot_id': self.lot_id_2.id, 'qty_done': float_round(self.qty_done_2, precision_rounding=workorder_line_id_2.product_uom_id.rounding or rounding)})

            if continue_production:
                self._create_subsequent_checks()
            elif float_compare(self.component_remaining_qty, 0, precision_rounding=rounding) < 0 and\
                    self.consumption == 'strict':
                # '< 0' as it's not possible to click on validate if qty_done < component_remaining_qty
                raise UserError(_('You should consume the quantity of %s defined in the BoM. If you want to consume more or less components, change the consumption setting on the BoM.') % self.component_id[0].name)
            elif float_compare(self.component_remaining_qty_2, 0, precision_rounding=rounding) < 0 and \
                    self.consumption == 'strict':
                # '< 0' as it's not possible to click on validate if qty_done < component_remaining_qty
                raise UserError(_('You should consume the quantity of %s defined in the BoM. If you want to consume more or less components, change the consumption setting on the BoM.') % self.component_id_2[0].name)

        if self.test_type == 'picture' and not self.picture:
            raise UserError(_('Please upload a picture.'))

        if self.test_type not in ('measure', 'passfail'):
            if self.current_quality_check_id:
                self.current_quality_check_id.do_pass()
            if self.current_quality_check_id_2:
                self.current_quality_check_id_2.do_pass()
        
        if self.skip_completed_checks:
            self._change_quality_check(increment=1, children=1, checks=self.skipped_check_ids)
        else:
            self._change_quality_check(increment=1, children=1)
