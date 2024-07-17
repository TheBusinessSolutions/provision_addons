# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import datetime

class FsmRecurring(models.Model):
    _inherit = 'fsm.recurring'


    contract_id = fields.Many2one('contract.contract')
    partner_id = fields.Many2one('res.partner')

    total_price_subtotal = fields.Float(related='contract_id.total_price_subtotal')
    show_order_amount = fields.Boolean(related='contract_id.show_order_amount')


    def add_single_visit(self):
        for rec in self:
            vals = rec._prepare_order_values(datetime.now().replace(microsecond=0))
            order = self.env["fsm.order"].create(vals)
            order._onchange_template_id()
