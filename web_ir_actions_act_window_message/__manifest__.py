# Copyright 2017 Therp BV, ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Client side message boxes",
    "version": "14.0.1.0.1",
    "author": "Therp BV, " "ACSONE SA/NV, " "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/web",
    "license": "AGPL-3",
    "category": "Hidden/Dependency",
    "summary": "Show a message box to users",
    "depends": ["web"],
    "data": ["security/ir.model.access.csv", "views/templates.xml"],
    "qweb": ["static/src/xml/web_ir_actions_act_window_message.xml"],
}
