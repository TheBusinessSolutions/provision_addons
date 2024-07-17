# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError

class FsmRecurring(models.Model):
    _inherit = 'fsm.recurring'


    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("progress", "Active"),
            ("suspend", "Suspended"),
            ("close", "Closed"),
        ],
        readonly=True,
        default="draft",
        tracking=True,
    )


    contact_id = fields.Many2one(
        "res.partner",
        string="Primary Contact",
        related='location_id.contact_id'
    )
    phone = fields.Char(string="Phone", related='location_id.phone')
