# -*- coding: utf-8 -*-
{
    'name': "CIS AMREIN App",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Arkeup",
    'website': "www.arkeup.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['cisamrein_base', 'cisamrein_product', 'cisamrein_stock', 'cisamrein_sale', 'cisamrein_purchase', 'cisamrein_account',
                'repair', 'mrp', 'hr', 'purchase_request', 'purchase_request_tier_validation'],
    'sequence': 1,
    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    'application': True,
}
