# -*- coding: utf-8 -*-
{
    'name': "Contract Link Field Service Recurring",

    'summary': """
        Contract Link Field Service Recurring""",

    'description': """
        Contract Link Field Service Recurring
    """,

    'author': "Salama",
    'website': "https://www.google.com",

    'category': 'FieldService',
    'version': '14.0',

    # any module necessary for this one to work correctly
    'depends': ['fieldservice_recurring','contract','sale'],

    # always loaded
    'data': [
        'views/views.xml',
    ],
}