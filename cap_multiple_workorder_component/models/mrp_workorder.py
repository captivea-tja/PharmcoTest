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
    test_type_2 = fields.Char(related='test_type_2_id.technical_name')
    user_id_2 = fields.Many2one(related='current_quality_check_id_2.user_id', readonly=False)
    picture_2 = fields.Binary(related='current_quality_check_id_2.picture', readonly=False)
    measure_2 = fields.Float(related='current_quality_check_id_2.measure', readonly=False)
    measure_success_2 = fields.Selection(related='current_quality_check_id_2.measure_success', readonly=False)
    norm_unit_2 = fields.Char(related='current_quality_check_id_2.norm_unit', readonly=False)
    component_qty_to_do_2 = fields.Float(compute='_compute_component_qty_to_do')

    current_quality_check_id_3 = fields.Many2one(
        'quality.check', "Current Quality Check", store=True, check_company=True)
    component_id_3 = fields.Many2one('product.product', related='current_quality_check_id_3.component_id')
    component_tracking_3 = fields.Selection(related='component_id_3.tracking', string="Is Component Tracked", readonly=False)
    component_remaining_qty_3 = fields.Float('Remaining Quantity for Component', compute='_compute_component_data', digits='Product Unit of Measure')
    component_uom_id_3 = fields.Many2one('uom.uom', compute='_compute_component_data', string="Component UoM")
    control_date_3 = fields.Datetime(related='current_quality_check_id_3.control_date', readonly=False)
    lot_id_3 = fields.Many2one(related='current_quality_check_id_3.lot_id', readonly=False)
    workorder_line_id_3 = fields.Many2one(related='current_quality_check_id_3.workorder_line_id', readonly=False)
    note_3 = fields.Html(related='current_quality_check_id_3.note')
    quality_state_3 = fields.Selection(related='current_quality_check_id_3.quality_state', string="Quality State", readonly=False)
    qty_done_3 = fields.Float(related='current_quality_check_id_3.qty_done', readonly=False)
    test_type_3_id = fields.Many2one('quality.point.test_type', 'Test Type', related='current_quality_check_id_3.test_type_id')
    test_type_3 = fields.Char(related='test_type_3_id.technical_name')
    user_id_3 = fields.Many2one(related='current_quality_check_id_3.user_id', readonly=False)
    picture_3 = fields.Binary(related='current_quality_check_id_3.picture', readonly=False)
    measure_3 = fields.Float(related='current_quality_check_id_3.measure', readonly=False)
    measure_success_3 = fields.Selection(related='current_quality_check_id_3.measure_success', readonly=False)
    norm_unit_3 = fields.Char(related='current_quality_check_id_3.norm_unit', readonly=False)
    component_qty_to_do_3 = fields.Float(compute='_compute_component_qty_to_do')

    current_quality_check_id_4 = fields.Many2one(
        'quality.check', "Current Quality Check", store=True, check_company=True)
    component_id_4 = fields.Many2one('product.product', related='current_quality_check_id_4.component_id')
    component_tracking_4 = fields.Selection(related='component_id_4.tracking', string="Is Component Tracked", readonly=False)
    component_remaining_qty_4 = fields.Float('Remaining Quantity for Component', compute='_compute_component_data', digits='Product Unit of Measure')
    component_uom_id_4 = fields.Many2one('uom.uom', compute='_compute_component_data', string="Component UoM")
    control_date_4 = fields.Datetime(related='current_quality_check_id_4.control_date', readonly=False)
    lot_id_4 = fields.Many2one(related='current_quality_check_id_4.lot_id', readonly=False)
    workorder_line_id_4 = fields.Many2one(related='current_quality_check_id_4.workorder_line_id', readonly=False)
    note_4 = fields.Html(related='current_quality_check_id_4.note')
    quality_state_4 = fields.Selection(related='current_quality_check_id_4.quality_state', string="Quality State", readonly=False)
    qty_done_4 = fields.Float(related='current_quality_check_id_4.qty_done', readonly=False)
    test_type_4_id = fields.Many2one('quality.point.test_type', 'Test Type', related='current_quality_check_id_4.test_type_id')
    test_type_4 = fields.Char(related='test_type_4_id.technical_name')
    user_id_4 = fields.Many2one(related='current_quality_check_id_4.user_id', readonly=False)
    picture_4 = fields.Binary(related='current_quality_check_id_4.picture', readonly=False)
    measure_4 = fields.Float(related='current_quality_check_id_4.measure', readonly=False)
    measure_success_4 = fields.Selection(related='current_quality_check_id_4.measure_success', readonly=False)
    norm_unit_4 = fields.Char(related='current_quality_check_id_4.norm_unit', readonly=False)
    component_qty_to_do_4 = fields.Float(compute='_compute_component_qty_to_do')

    current_quality_check_id_5 = fields.Many2one(
        'quality.check', "Current Quality Check", store=True, check_company=True)
    component_id_5 = fields.Many2one('product.product', related='current_quality_check_id_5.component_id')
    component_tracking_5 = fields.Selection(related='component_id_5.tracking', string="Is Component Tracked", readonly=False)
    component_remaining_qty_5 = fields.Float('Remaining Quantity for Component', compute='_compute_component_data', digits='Product Unit of Measure')
    component_uom_id_5 = fields.Many2one('uom.uom', compute='_compute_component_data', string="Component UoM")
    control_date_5 = fields.Datetime(related='current_quality_check_id_5.control_date', readonly=False)
    lot_id_5 = fields.Many2one(related='current_quality_check_id_5.lot_id', readonly=False)
    workorder_line_id_5 = fields.Many2one(related='current_quality_check_id_5.workorder_line_id', readonly=False)
    note_5 = fields.Html(related='current_quality_check_id_5.note')
    quality_state_5 = fields.Selection(related='current_quality_check_id_5.quality_state', string="Quality State", readonly=False)
    qty_done_5 = fields.Float(related='current_quality_check_id_5.qty_done', readonly=False)
    test_type_5_id = fields.Many2one('quality.point.test_type', 'Test Type', related='current_quality_check_id_5.test_type_id')
    test_type_5 = fields.Char(related='test_type_5_id.technical_name')
    user_id_5 = fields.Many2one(related='current_quality_check_id_5.user_id', readonly=False)
    picture_5 = fields.Binary(related='current_quality_check_id_5.picture', readonly=False)
    measure_5 = fields.Float(related='current_quality_check_id_5.measure', readonly=False)
    measure_success_5 = fields.Selection(related='current_quality_check_id_5.measure_success', readonly=False)
    norm_unit_5 = fields.Char(related='current_quality_check_id_5.norm_unit', readonly=False)
    component_qty_to_do_5 = fields.Float(compute='_compute_component_qty_to_do')


    test_type_all = fields.Boolean(compute='_compute_test_type_components_all')
    component_qty_to_do_all = fields.Float(compute='_compute_test_type_components_all')

    @api.depends('test_type', 'test_type_2', 'test_type_3', 'test_type_4', 'test_type_5', 'component_remaining_qty', 'component_remaining_qty_2', 'component_remaining_qty_3', 'component_remaining_qty_4', 'component_remaining_qty_5')
    def _compute_test_type_components_all(self):
        reg_list = ['register_byproducts', 'register_consumed_materials']
        for wo in self:
            test_type_all = False
            component_qty_to_do_all = False

            if wo.test_type not in reg_list and wo.test_type_2 not in reg_list and wo.test_type_3 not in reg_list and wo.test_type_4 not in reg_list and wo.test_type_5 not in reg_list:
                test_type_all = True
            if wo.component_qty_to_do < 0 and wo.component_qty_to_do_2 < 0 and wo.component_qty_to_do_3 < 0 and wo.component_qty_to_do_4 < 0 and wo.component_qty_to_do_5 < 0:
               component_qty_to_do_all = -1
            if wo.component_qty_to_do > 0 and wo.component_qty_to_do_2 > 0 and wo.component_qty_to_do_3 > 0 and wo.component_qty_to_do_4 > 0 and wo.component_qty_to_do_5 > 0:
               component_qty_to_do_all = 1

            wo.test_type_all = test_type_all
            wo.component_qty_to_do_all = component_qty_to_do_all

    @api.depends('component_qty_to_do', 'component_qty_to_do_2', 'component_qty_to_do_3', 'component_qty_to_do_4', 'component_qty_to_do_5')
    def _compute_component_qty_to_do(self):
        res = super(MrpProductionWorkcenterLine, self)._compute_component_qty_to_do()
        for wo in self:
            wo.component_qty_to_do = wo.qty_done - wo.component_remaining_qty

            wo.component_qty_to_do_2 = wo.qty_done_2 - wo.component_remaining_qty_2

            wo.component_qty_to_do_3 = wo.qty_done_3 - wo.component_remaining_qty_3

            wo.component_qty_to_do_4 = wo.qty_done_4 - wo.component_remaining_qty_4

            wo.component_qty_to_do_5 = wo.qty_done_5 - wo.component_remaining_qty_5

        return res


    def _compute_component_data(self):
        '''
        Overwritten this function to manage multiple components to proceed with the consumption on same order.
        '''
        res = super(MrpProductionWorkcenterLine, self)._compute_component_data()
        self.component_remaining_qty = False
        self.component_uom_id = False

        self.component_remaining_qty_2 = False
        self.component_uom_id_2 = False

        self.component_remaining_qty_3 = False
        self.component_uom_id_3 = False

        self.component_remaining_qty_4 = False
        self.component_uom_id_4 = False

        self.component_remaining_qty_5 = False
        self.component_uom_id_5 = False

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

                move_3 = wo.current_quality_check_id_3.workorder_line_id.move_id
                lines_3 = wo._workorder_line_ids().filtered(lambda l: l.move_id == move_3)
                completed_lines_3 = lines_3.filtered(lambda l: l.lot_id) if wo.component_id_3.tracking != 'none' else lines_3
                wo.component_remaining_qty_3 = self._prepare_component_quantity(move_3, wo.qty_producing) - sum(completed_lines_3.mapped('qty_done'))
                wo.component_uom_id_3 = lines[:1].product_uom_id

                move_4 = wo.current_quality_check_id_4.workorder_line_id.move_id
                lines_4 = wo._workorder_line_ids().filtered(lambda l: l.move_id == move_4)
                completed_lines_4 = lines_4.filtered(lambda l: l.lot_id) if wo.component_id_4.tracking != 'none' else lines_4
                wo.component_remaining_qty_4 = self._prepare_component_quantity(move_4, wo.qty_producing) - sum(completed_lines_4.mapped('qty_done'))
                wo.component_uom_id_4 = lines[:1].product_uom_id

                move_5 = wo.current_quality_check_id_5.workorder_line_id.move_id
                lines_5 = wo._workorder_line_ids().filtered(lambda l: l.move_id == move_5)
                completed_lines_5 = lines_5.filtered(lambda l: l.lot_id) if wo.component_id_5.tracking != 'none' else lines_5
                wo.component_remaining_qty_5 = self._prepare_component_quantity(move_5, wo.qty_producing) - sum(completed_lines_5.mapped('qty_done'))
                wo.component_uom_id_5 = lines[:1].product_uom_id

        return res

    def _change_quality_check(self, **params):
        """
        Inherited this function to manage other components to proceed with the consumption on same order.
        """
        self.ensure_one()
        res = super(MrpProductionWorkcenterLine, self)._change_quality_check()

        check_id_2 = None
        check_id_3 = None
        check_id_4 = None
        check_id_5 = None
        # Determine the list of checks to consider
        checks = params['checks'] if 'checks' in params else self.check_ids
        if not params.get('children'):
            checks = checks.filtered(lambda c: not c.parent_id)
        # We need to make sure the current quality check is in our list
        # when we compute position relatively to the current quality check.

        if 'increment' in params or 'checks' in params and self.current_quality_check_id not in checks:
            checks |= self.current_quality_check_id

        if 'increment' in params or 'checks' in params and self.current_quality_check_id_2 not in checks:
            checks |= self.current_quality_check_id_2

        if 'increment' in params or 'checks' in params and self.current_quality_check_id_3 not in checks:
            checks |= self.current_quality_check_id_3

        if 'increment' in params or 'checks' in params and self.current_quality_check_id_4 not in checks:
            checks |= self.current_quality_check_id_4

        if 'increment' in params or 'checks' in params and self.current_quality_check_id_5 not in checks:
            checks |= self.current_quality_check_id_5

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
            from_last_step = not self.current_quality_check_id and not self.current_quality_check_id_2 and not self.current_quality_check_id_3 and not self.current_quality_check_id_4 and not self.current_quality_check_id_5
            
            even = False
            if (order_check_len % 5) == 0:
                even = True

            starting_point = False
            if from_last_step and increment < 0:
                if not even:
                    sublist_ids = [ordered_check_ids[5*i:5*(i+1)] for i in range(int(len(ordered_check_ids)/5) + 1)]

                    starting_point = sublist_ids[-1] and sublist_ids[-1][0] is not False and sublist_ids[-1] or sublist_ids[-2]

            current_id = self.current_quality_check_id.id
            if current_id:
                if increment > 0:
                    increment += 4
                elif increment < 0:
                    increment -= 4

            position = ordered_check_ids.index(current_id)
            if params.get('increment') < 0 and position and not from_last_step:
                position = position - 5
            elif params.get('increment') < 0 and from_last_step and starting_point:
                position = ordered_check_ids.index(starting_point[0])
            else:
                position = position + increment
            if position in range(0, order_check_len):
                check_id = ordered_check_ids[position]
            else:
                check_id = False
            
            current_id_2 = self.current_quality_check_id_2.id
            position_2 = ordered_check_ids.index(current_id_2)
            position_2 = position + 1
            
            if position_2 in range(0, order_check_len):
                if check_id != ordered_check_ids[position_2]:
                    check_id_2 = ordered_check_ids[position_2]
                else:
                    check_id_2 = False
            else:
                check_id_2 = False

            current_id_3 = self.current_quality_check_id_3.id
            position_3 = ordered_check_ids.index(current_id_3)
            position_3 = position_2 + 1

            if position_3 in range(0, order_check_len):
                if check_id != ordered_check_ids[position_3]:
                    check_id_3 = ordered_check_ids[position_3]
                else:
                    check_id_3 = False
            else:
                check_id_3 = False

            current_id_4 = self.current_quality_check_id_4.id
            position_4 = ordered_check_ids.index(current_id_4)
            position_4 = position_3 + 1

            if position_4 in range(0, order_check_len):
                if check_id != ordered_check_ids[position_4]:
                    check_id_4 = ordered_check_ids[position_4]
                else:
                    check_id_4 = False
            else:
                check_id_4 = False

            current_id_5 = self.current_quality_check_id_5.id
            position_5 = ordered_check_ids.index(current_id_5)
            position_5 = position_4 + 1

            if position_5 in range(0, order_check_len):
                if check_id != ordered_check_ids[position_5]:
                    check_id_5 = ordered_check_ids[position_5]
                else:
                    check_id_5 = False
            else:
                check_id_5 = False

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

            position_3 = position_2
            if position_2 < 0:
                position_3 -= 1
            if position_2 >= 0:
                position_3 += 1
            if position_3 in range(0, order_check_len):
                if check_id != ordered_check_ids[position_3]:
                    check_id_3 = ordered_check_ids[position_3]
                else:
                    check_id_3 = False
            else:
                check_id_3 = False

            position_4 = position_3
            if position_3 < 0:
                position_4 -= 1
            if position_3 >= 0:
                position_4 += 1
            if position_4 in range(0, order_check_len):
                if check_id != ordered_check_ids[position_4]:
                    check_id_4 = ordered_check_ids[position_4]
                else:
                    check_id_4 = False
            else:
                check_id_4 = False

            position_5 = position_4
            if position_4 < 0:
                position_5 -= 1
            if position_4 >= 0:
                position_5 += 1
            if position_5 in range(0, order_check_len):
                if check_id != ordered_check_ids[position_5]:
                    check_id_5 = ordered_check_ids[position_5]
                else:
                    check_id_5 = False
            else:
                check_id_5 = False

        elif params.get('goto') in ordered_check_ids:
            check_id = params['goto']
            position = ordered_check_ids.index(check_id)

            position_2 = position + 1
            if position_2 in range(0, order_check_len):
                check_id_2 = ordered_check_ids[position_2]
            else: 
                check_id_2 = False

            position_3 = position_2 + 1
            if position_3 in range(0, order_check_len):
                check_id_3 = ordered_check_ids[position_3]
            else:
                check_id_3 = False

            position_4 = position_3 + 1
            if position_4 in range(0, order_check_len):
                check_id_4 = ordered_check_ids[position_4]
            else:
                check_id_4 = False
        
            position_5 = position_4 + 1
            if position_5 in range(0, order_check_len):
                check_id_5 = ordered_check_ids[position_5]
            else:
                check_id_5 = False

        # Change the quality check and the worksheet page if necessary
        if check_id_2 is not None or check_id_3 is not None or check_id_4 is not None or check_id_5 is not None:
            next_check_2 = self.env['quality.check'].browse(check_id_2)
            change_worksheet_page = position_2 != order_check_len and next_check_2.point_id.worksheet == 'scroll'

            next_check_3 = self.env['quality.check'].browse(check_id_3)
            change_worksheet_page = position_3 != order_check_len and next_check_3.point_id.worksheet == 'scroll'

            next_check_4 = self.env['quality.check'].browse(check_id_4)
            change_worksheet_page = position_4 != order_check_len and next_check_4.point_id.worksheet == 'scroll'

            next_check_5 = self.env['quality.check'].browse(check_id_5)
            change_worksheet_page = position_5 != order_check_len and next_check_5.point_id.worksheet == 'scroll'

            checks = self.check_ids.filtered(lambda c: c.finished_product_sequence == self.qty_produced)
            # curr_pos = params.get('position') and params.get('position') + 1
            curr_pos = params.get('position')

            vals = {
                'allow_producing_quantity_change': True if curr_pos == 0 and all(c.quality_state == 'none' for c in checks) else False,
                'current_quality_check_id': check_id,
                'current_quality_check_id_2': check_id_2,
                'current_quality_check_id_3': check_id_3,
                'current_quality_check_id_4': check_id_4,
                'current_quality_check_id_5': check_id_5,
                'is_first_step': position == 0 or position_2 == 0 or position_3 == 0 or position_4 == 0 or position_5 == 0,
                'is_last_step': check_id == False and check_id_2 == False and check_id_3 == False and check_id_4 == False and check_id_5 == False,
                'worksheet_page': next_check_5.point_id.worksheet_page if change_worksheet_page else self.worksheet_page,
            }

            self.write(vals)
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
        workorder_line_id_3 = self.current_quality_check_id_3.workorder_line_id
        workorder_line_id_4 = self.current_quality_check_id_4.workorder_line_id
        workorder_line_id_5 = self.current_quality_check_id_5.workorder_line_id
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
            if self.component_tracking_3 != 'none' and not self.lot_id_3 and self.qty_done_3 != 0:
                raise UserError(_('Please enter a Lot/SN.'))
            if self.component_tracking_4 != 'none' and not self.lot_id_4 and self.qty_done_4 != 0:
                raise UserError(_('Please enter a Lot/SN.'))
            if self.component_tracking_5 != 'none' and not self.lot_id_5 and self.qty_done_5 != 0:
                raise UserError(_('Please enter a Lot/SN.'))
            if float_compare(self.qty_done, 0, precision_rounding=rounding) < 0:
                raise UserError(_('Please enter a positive quantity.'))
            if float_compare(self.qty_done_2, 0, precision_rounding=rounding) < 0:
                raise UserError(_('Please enter a positive quantity.'))
            if float_compare(self.qty_done_3, 0, precision_rounding=rounding) < 0:
                raise UserError(_('Please enter a positive quantity.'))
            if float_compare(self.qty_done_4, 0, precision_rounding=rounding) < 0:
                raise UserError(_('Please enter a positive quantity.'))
            if float_compare(self.qty_done_5, 0, precision_rounding=rounding) < 0:
                raise UserError(_('Please enter a positive quantity.'))

            # Get the move lines associated with our component
            self.component_remaining_qty -= float_round(self.qty_done, precision_rounding=self.workorder_line_id.product_uom_id.rounding or rounding)
            self.component_remaining_qty_2 -= float_round(self.qty_done_2, precision_rounding=workorder_line_id_2.product_uom_id.rounding or rounding)
            self.component_remaining_qty_3 -= float_round(self.qty_done_3, precision_rounding=workorder_line_id_3.product_uom_id.rounding or rounding)
            self.component_remaining_qty_4 -= float_round(self.qty_done_4, precision_rounding=workorder_line_id_4.product_uom_id.rounding or rounding)
            self.component_remaining_qty_5 -= float_round(self.qty_done_5, precision_rounding=workorder_line_id_5.product_uom_id.rounding or rounding)

            # Write the lot and qty to the move line
            self.workorder_line_id.write({'lot_id': self.lot_id.id, 'qty_done': float_round(self.qty_done, precision_rounding=self.workorder_line_id.product_uom_id.rounding or rounding)})
            workorder_line_id_2.write({'lot_id': self.lot_id_2.id, 'qty_done': float_round(self.qty_done_2, precision_rounding=workorder_line_id_2.product_uom_id.rounding or rounding)})
            workorder_line_id_3.write({'lot_id': self.lot_id_3.id, 'qty_done': float_round(self.qty_done_3, precision_rounding=workorder_line_id_3.product_uom_id.rounding or rounding)})
            workorder_line_id_4.write({'lot_id': self.lot_id_4.id, 'qty_done': float_round(self.qty_done_4, precision_rounding=workorder_line_id_4.product_uom_id.rounding or rounding)})
            workorder_line_id_5.write({'lot_id': self.lot_id_5.id, 'qty_done': float_round(self.qty_done_5, precision_rounding=workorder_line_id_5.product_uom_id.rounding or rounding)})

            if continue_production:
                self._create_subsequent_checks()
            elif self.component_id and float_compare(self.component_remaining_qty, 0, precision_rounding=rounding) < 0 and\
                    self.consumption == 'strict':
                # '< 0' as it's not possible to click on validate if qty_done < component_remaining_qty
                raise UserError(_('You should consume the quantity of %s defined in the BoM. If you want to consume more or less components, change the consumption setting on the BoM.') % (self.component_id and self.component_id[0].name or ''))
            elif self.component_id_2 and float_compare(self.component_remaining_qty_2, 0, precision_rounding=rounding) < 0 and \
                    self.consumption == 'strict':
                # '< 0' as it's not possible to click on validate if qty_done < component_remaining_qty
                raise UserError(_('You should consume the quantity of %s defined in the BoM. If you want to consume more or less components, change the consumption setting on the BoM.') % (self.component_id_2 and self.component_id_2[0].name or ''))
            elif self.component_id_3 and float_compare(self.component_remaining_qty_3, 0, precision_rounding=rounding) < 0 and \
                    self.consumption == 'strict':
                # '< 0' as it's not possible to click on validate if qty_done < component_remaining_qty
                raise UserError(_('You should consume the quantity of %s defined in the BoM. If you want to consume more or less components, change the consumption setting on the BoM.') % (self.component_id_3 and self.component_id_3[0].name or ''))
            elif self.component_id_4 and float_compare(self.component_remaining_qty_4, 0, precision_rounding=rounding) < 0 and \
                    self.consumption == 'strict':
                # '< 0' as it's not possible to click on validate if qty_done < component_remaining_qty
                raise UserError(_('You should consume the quantity of %s defined in the BoM. If you want to consume more or less components, change the consumption setting on the BoM.') % (self.component_id_4 and self.component_id_4[0].name or ''))

            elif self.component_id_5 and float_compare(self.component_remaining_qty_5, 0, precision_rounding=rounding) < 0 and \
                    self.consumption == 'strict':
                # '< 0' as it's not possible to click on validate if qty_done < component_remaining_qty
                raise UserError(_('You should consume the quantity of %s defined in the BoM. If you want to consume more or less components, change the consumption setting on the BoM.') % (self.component_id_5 and self.component_id_5[0].name or ''))

        if self.test_type == 'picture' and not self.picture:
            raise UserError(_('Please upload a picture.'))

        if self.test_type not in ('measure', 'passfail'):
            if self.current_quality_check_id:
                self.current_quality_check_id.do_pass()
            if self.current_quality_check_id_2:
                self.current_quality_check_id_2.do_pass()
            if self.current_quality_check_id_3:
                self.current_quality_check_id_3.do_pass()
            if self.current_quality_check_id_4:
                self.current_quality_check_id_4.do_pass()
            if self.current_quality_check_id_5:
                self.current_quality_check_id_5.do_pass()
        
        if self.skip_completed_checks:
            self._change_quality_check(increment=1, children=1, checks=self.skipped_check_ids)
        else:
            self._change_quality_check(increment=1, children=1)

        if continue_production and self.component_remaining_qty <= 0 and self.component_remaining_qty_2 <= 0 and self.component_remaining_qty_3 <= 0 and self.component_remaining_qty_4 <= 0 and self.component_remaining_qty_5 <= 0:
            if self.skip_completed_checks:
                self._change_quality_check(increment=1, children=1, checks=self.skipped_check_ids)
            else:
                self._change_quality_check(increment=1, children=1)

    def _create_subsequent_checks(self):
        """ When processing a step with regiter a consumed material
        that's a lot we will some times need to create a new
        intermediate check.
        e.g.: Register 2 product A tracked by SN. We will register one
        with the current checks but we need to generate a second step
        for the second SN. Same for lot if the user wants to use more
        than one lot.
        """
        # Create another quality check if necessary

        quality_check_id_ids = []
        if self.current_quality_check_id and self.current_quality_check_id.component_id.tracking == 'serial':
            quality_check_id_ids.append(self.current_quality_check_id)
        if self.current_quality_check_id_2 and self.current_quality_check_id_2.component_id.tracking == 'serial':
            quality_check_id_ids.append(self.current_quality_check_id_2)
        if self.current_quality_check_id_3 and self.current_quality_check_id_3.component_id.tracking == 'serial':
            quality_check_id_ids.append(self.current_quality_check_id_3)
        if self.current_quality_check_id_4 and self.current_quality_check_id_4.component_id.tracking == 'serial':
            quality_check_id_ids.append(self.current_quality_check_id_4)
        if self.current_quality_check_id_5 and self.current_quality_check_id_5.component_id.tracking == 'serial':
            quality_check_id_ids.append(self.current_quality_check_id_5)


        for current_quality_check in quality_check_id_ids:
            parent_id = current_quality_check
            if parent_id.parent_id:
                parent_id = parent_id.parent_id
            subsequent_substeps = self.env['quality.check'].search([('parent_id', '=', parent_id.id), ('id', '>', current_quality_check.id)])
            if not subsequent_substeps:
                # Split current workorder line.
                rounding = self.workorder_line_id.product_uom_id.rounding
                if float_compare(self.workorder_line_id.qty_done, self.workorder_line_id.qty_to_consume, precision_rounding=rounding) < 0:
                    self.workorder_line_id.copy(default={'qty_done': 0, 'qty_to_consume': self.workorder_line_id.qty_to_consume - self.workorder_line_id.qty_done})
                    self.workorder_line_id.write({'qty_to_consume': self.workorder_line_id.qty_done})
                # Check if it exists a workorder line not used. If it could not find
                # one, create it without prefilled values.
                elif not self._defaults_from_workorder_lines(self.workorder_line_id.move_id, self.test_type):
                    moves = self.env['stock.move']
                    workorder_line_values = {}
                    if self.test_type == 'register_byproducts':
                        moves |= self.move_finished_ids.filtered(lambda m: m.state not in ('done', 'cancel') and m.product_id == self.component_id)
                        workorder_line_values['finished_workorder_id'] = self.id
                    else:
                        moves = self.move_raw_ids.filtered(lambda m: m.state not in ('done', 'cancel') and m.product_id == self.component_id)
                        workorder_line_values['raw_workorder_id'] = self.id
                    workorder_line_values.update({
                        'move_id': moves[:1].id,
                        'product_id': self.component_id.id,
                        'product_uom_id': moves[:1].product_uom.id,
                        'qty_done': 0.0,
                    })
                    self.env['mrp.workorder.line'].create(workorder_line_values)
                # Creating quality checks
                quality_check_data = {
                    'workorder_id': self.id,
                    'product_id': self.product_id.id,
                    'company_id': self.company_id.id,
                    'parent_id': parent_id.id,
                    'finished_product_sequence': self.qty_produced,
                }
                if current_quality_check.point_id:
                    quality_check_data.update({
                        'point_id': current_quality_check.point_id.id,
                        'team_id': current_quality_check.point_id.team_id.id,
                    })
                else:
                    quality_check_data.update({
                        'component_id': current_quality_check.component_id.id,
                        'test_type_id': current_quality_check.test_type_id.id,
                        'team_id': current_quality_check.team_id.id,
                    })
                move = parent_id.workorder_line_id.move_id
                quality_check_data.update(self._defaults_from_workorder_lines(move, current_quality_check.test_type))
                check_created = self.env['quality.check'].create(quality_check_data)
