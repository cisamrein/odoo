# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StockPickingInherit(models.Model):
    _inherit = 'stock.picking'

    include_document = fields.Text()
    cmd_customer_ref = fields.Char()

    def print_conformity_statement(self):
        return self.env.ref('cisamrein_sale.report_conformity_statement').report_action(self)