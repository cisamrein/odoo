# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductCustomerRef(models.Model):
    _name = 'product.customer.ref'
    _description = 'Reference of product for customer'

    name = fields.Char(string='Reference')
    partner_id = fields.Many2one('res.partner', domain=[('customer_rank' ,'>', 0)], string='Customer', required=True)
    product_tmpl_id = fields.Many2one('product.template')
