# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    include_document = fields.Text()

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    customer_reference = fields.Char(store=True)
