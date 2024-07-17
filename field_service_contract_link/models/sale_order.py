# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = 'sale.order'


    def button_open_customer_contract(self):
        ''' Redirect the user to this order Customer Contracts.
        :return:    An action on contract.contract.
        '''
        self.ensure_one()
        return {
            'name': _("Customer Contracts"),
            'type': 'ir.actions.act_window',
            'res_model': 'contract.contract',
            'views': [(self.env.ref('contract.contract_contract_tree_view').id,'tree'), (self.env.ref('contract.contract_contract_customer_form_view').id, 'form')],
            'context': {
                'default_partner_id': self.partner_id.id,
                'default_name': self.name,
                'default_company_id': self.company_id.id,
                'default_order_id': self.id,
                },
            'view_mode': 'list,form',
            'domain': [('order_id', '=', self.id)],
        }