# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError

class FsmOrder(models.Model):
    _inherit = 'fsm.order'

    contact_id = fields.Many2one(
        "res.partner",
        string="Primary Contact",
        related='fsm_recurring_id.contact_id'
    )
    phone = fields.Char(string="Phone", related='fsm_recurring_id.phone')
