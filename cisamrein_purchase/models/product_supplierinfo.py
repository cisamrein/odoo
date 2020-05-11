# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ProductSupplierInfo(models.Model):
    _name = 'product.supplierinfo'
    _inherit = ['product.supplierinfo', 'mail.thread']

    date_start = fields.Date('Start Date', help="Start date for this vendor price", tracking=True)
    date_end = fields.Date('End Date', help="End date for this vendor price", tracking=True)
