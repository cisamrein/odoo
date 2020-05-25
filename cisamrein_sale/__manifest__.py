# -*- coding: utf-8 -*-
{
    'name': "CIS AMREIN Sales",

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
    'category': 'Sales/Sales',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['web', 'sale_management', 'cisamrein_stock'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'views/product_customer_ref_views.xml',
        'views/product_template_views.xml',
        'views/stock_picking_views.xml',
        'views/view_config_settings.xml',
        'views/sale_order_views.xml',
        'report/conformity_statement_report.xml',
        'report/conformity_statement_template.xml',
        'report/stock_picking_template.xml',
        'report/order_quotation_inherit.xml',
    ]
}

