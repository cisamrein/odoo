# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    include_document = fields.Text()
    cmd_customer_ref = fields.Char()