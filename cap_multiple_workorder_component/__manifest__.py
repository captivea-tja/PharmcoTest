# -*- coding: utf-8 -*-
{
    'name': "Cap Multiple Components on Workorders",

    'summary': """
        Allows to work with 5 components on workorder at a time""",

    'description': """
        Allows to work with 5 components on workorder at a time""",

    'author': 'Captivea',
    'website': 'www.captivea.us',
    'version': '13.0.1.0.0',
    'category': 'Manufacturing/Manufacturing',

    # any module necessary for this one to work correctly
    'depends': ['mrp_workorder', 'quality_control'],

    # always loaded
    'data': [
        'views/mrp_workorder_views.xml',
    ],

}