# -*- coding: utf-8 -*-
{
    'name': "Cap Auto Assign Lots / Serails",

    'summary': """
        Allows to work with 5 components on workorder at a time""",

    'description': """
        Allows to work with 5 components on workorder at a time""",

    'author': 'Captivea',
    'website': 'www.captivea.us',
    'version': '13.0.1.0.0',
    'category': 'Manufacturing/Manufacturing',

    # any module necessary for this one to work correctly
    'depends': ['stock'],

    # always loaded
    'data': [
        'views/view_stock_move_line.xml',
    ],

}