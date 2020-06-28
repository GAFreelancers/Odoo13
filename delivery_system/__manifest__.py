# -*- coding: utf-8 -*-
{
    'name': "Delivery System",

    'summary': """
         Effective delivery system """,

    'description': """
        Long description of module's purpose
    """,

    'author': "Muhammed Fazil",
    'website': "http://www.odoo.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Industries',
    'version': '13.0.1.0',

    # any module necessary for this one to work correctly
    'depends': ['base','crm','stock','sale','account','board'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/view.xml',
        'views/sequence.xml',
        # 'views/dashboard.xml',
        # 'report/report_conn.xml',
        # 'report/report_template.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
    ],
     'installable': True,
    'application': True,
    'auto_install': False,

}
