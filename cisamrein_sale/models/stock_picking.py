# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StockPickingInherit(models.Model):
    _inherit = 'stock.picking'

    include_document = fields.Text()
    cmd_customer_ref = fields.Char(related="sale_id.cmd_customer_ref")