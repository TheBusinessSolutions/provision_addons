# -*- coding: utf-8 -*-
from odoo import api,fields,models,_

class FsmLocation(models.Model):
    _inherit = "fsm.location"

    location_link = fields.Char()


class FsmOrder(models.Model):
    _inherit = "fsm.order"

    location_link = fields.Char(related='location_id.location_link')


    # Need to Comment display_name in (fieldservice model)
    # display_name = fields.Char(string="Order")
    def name_get(self):
        ret_list = []
        for line in self.sudo():
            name = str(line.name) + ' (' + str(line.location_id.name) +')'
            ret_list.append((line.id, name))
        return ret_list