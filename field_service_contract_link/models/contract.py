# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError

class ContractContract(models.Model):
    _inherit = 'contract.contract'

    order_id = fields.Many2one('sale.order')


    def _default_team_id(self):
        return self.env.ref("fieldservice.fsm_team_default")


    fsm_recurring_template_id = fields.Many2one(
        "fsm.recurring.template",
        "Recurring Template",
    )

    fsm_order_template_id = fields.Many2one(
        "fsm.template",
        string="Order Template",
        help="This is the order template that will be recurring",
    )

    fsm_frequency_set_id = fields.Many2one("fsm.frequency.set", "Frequency Set")

    scheduled_duration = fields.Float(
        string="Scheduled duration", help="Scheduled duration of the work in hours"
    )

    max_orders = fields.Integer(
        string="Maximum Orders", help="Maximium number of orders that will be created"
    )

    location_id = fields.Many2one(
        "fsm.location", string="Location", index=True, required=True
    )

    contact_id = fields.Many2one(
        "res.partner",
        string="Primary Contact",
        related='location_id.contact_id'
    )
    phone = fields.Char(string="Phone", related='location_id.phone')

    team_id = fields.Many2one(
        "fsm.team",
        string="Team",
        default=lambda self: self._default_team_id(),
        index=True,
        required=True,
        tracking=True,
    )

    person_id = fields.Many2one(
        "fsm.person", string="Assigned To", index=True, tracking=True
    )
    

    @api.onchange("fsm_recurring_template_id")
    def onchange_recurring_template_id(self):
        if not self.fsm_recurring_template_id:
            return
        values = self.populate_from_template()
        self.update(values)

    def populate_from_template(self, template=False):
        if not template:
            template = self.fsm_recurring_template_id
        vals = {
            "fsm_frequency_set_id": template.fsm_frequency_set_id,
            "max_orders": template.max_orders,
            # "description": template.description,
            "fsm_order_template_id": template.fsm_order_template_id,
            "scheduled_duration": template.fsm_order_template_id.duration,
            "company_id": template.company_id.id,
        }
        return vals

    
    show_order_amount = fields.Boolean()
    total_price_subtotal = fields.Float(compute="get_total_price")
    def get_total_price(self):
        for this in self:
            this.total_price_subtotal = 0
            if len(this.contract_line_fixed_ids)>0:
                this.total_price_subtotal = sum(this.contract_line_fixed_ids.mapped('price_subtotal'))


    def button_open_field_service_recurring(self):
        ''' Redirect the user to this order Field Service Recurring.
        :return:    An action on fsm.recurring.
        '''
        self.ensure_one()
        return {
            'name': _("Contracts and Subscription"),
            'type': 'ir.actions.act_window',
            'res_model': 'fsm.recurring',
            'context': {
                'default_contract_id': self.id,
                'default_partner_id': self.partner_id.id,
                'default_fsm_recurring_template_id': self.fsm_recurring_template_id.id,
                'default_fsm_order_template_id': self.fsm_order_template_id.id,
                'default_fsm_frequency_set_id': self.fsm_frequency_set_id.id,
                'default_scheduled_duration': self.scheduled_duration,
                'default_start_date': self.date_start,
                'default_end_date': self.date_end,
                'default_max_orders': self.max_orders,
                'default_location_id': self.location_id.id,
                'default_team_id': self.team_id.id,
                'default_person_id': self.person_id.id,
                'default_company_id': self.company_id.id,
                },
            'view_mode': 'list,form',
            'domain': [('contract_id', '=', self.id)],
        }