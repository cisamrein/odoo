# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ProductSupplierInfo(models.Model):
    _name = 'product.supplierinfo'
    _inherit = ['product.supplierinfo', 'mail.thread']

    date_start = fields.Date('Start Date', help="Start date for this vendor price", tracking=True)
    date_end = fields.Date('End Date', help="End date for this vendor price", tracking=True)
    price = fields.Float(
        'Price', default=0.0, digits='Product Price',
        required=True, help="The price to purchase a product", tracking=True)
    min_qty = fields.Float(
        'Quantity', default=0.0, required=True, tracking=True,
        help="The quantity to purchase from this vendor to benefit from the price, expressed in the vendor Product Unit of Measure if not any, in the default unit of measure of the product otherwise.")

