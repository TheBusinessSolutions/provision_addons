# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import datetime

class FsmOrder(models.Model):
    _inherit = 'fsm.order'

    total_price_subtotal = fields.Float(related='fsm_recurring_id.total_price_subtotal')
    show_order_amount = fields.Boolean(related='fsm_recurring_id.show_order_amount')

    def action_complete(self):
        res = super().action_complete()
        self.write({"date_end": datetime.now(),})
        return res

    def action_cancel(self):
        res = super().action_cancel()
        self.write({"date_end": datetime.now(),})
        return res

    last_visit = fields.Datetime(compute="get_last_visit")
    def get_last_visit(self):
        for this in self:
            this.last_visit = False
            other_orders = self.fsm_recurring_id.fsm_order_ids
            if len(other_orders)>1 and this in other_orders:
                current_index = list(other_orders).index(this)

                if current_index > 0:
                    this.last_visit = other_orders[current_index - 1].date_end
