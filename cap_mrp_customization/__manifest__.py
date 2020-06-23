# -*- coding: utf-8 -*-
{
    'name': "Cap MRP Customizations",

    'summary': """
        Adds Manufacturer's Lot Number and Expiration Dates while receiving stock""",

    'description': """
        Adds Manufacturer's Lot Number and Expiration Dates while receiving stock""",

    'author': 'Captivea',
    'website': 'www.captivea.us',
    'version': '13.0.1.0.0',
    'category': 'Manufacturing/Manufacturing',

    # any module necessary for this one to work correctly
    'depends': ['mrp_workorder'],

    # always loaded
    'data': [
        'views/view_stock_move_line_inherited.xml',
        'views/stock_inventory_views.xml',
        'wizard/mrp_product_product_views.xml',
    ],

}