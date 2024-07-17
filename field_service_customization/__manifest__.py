# -*- coding: utf-8 -*-
{
    'name': "Fieldservice Order & Recurring",

    'summary': """
        Add fields & Change names in Fieldservice Order & Recurring""",

    'description': """
        Add fields & Change names in Fieldservice Order & Recurring
    """,

    'author': "Salama",
    'website': "https://www.google.com",

    'category': 'FieldService',
    'version': '14.0',

    # any module necessary for this one to work correctly
    'depends': ['fieldservice_recurring'],

    # always loaded
    'data': [
        'views/views.xml',
    ],
}