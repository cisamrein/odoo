# -*- coding: utf-8 -*-
{
    'name': "CIS AMREIN Invoice",

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
    'category': 'Operations/Accounting',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['account', 'cisamrein_base', 'purchase'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'report/report_invoice.xml',
        'data/ir_sequence_data.xml',
        'views/view_account_move.xml',
        'views/view_res_config_settings.xml',

    ],
}
