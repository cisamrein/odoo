# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductTemplateInherit(models.Model):
    _inherit = 'product.template'

    customer_reference_ids = fields.One2many('product.customer.ref', 'product_tmpl_id')