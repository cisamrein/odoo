# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StockPickingInherit(models.Model):
    _inherit = 'stock.picking'

    include_document = fields.Text()
    cmd_customer_ref = fields.Char()
    assignment_center_id = fields.Many2one("res.partner", compute='_compute_assignment_center', help="Add Assignment center on the Order")

    def print_conformity_statement(self):
        return self.env.ref('cisamrein_sale.report_conformity_statement').report_action(self)

    def _compute_assignment_center(self):
        for rec in self:
            if rec.sale_id:
                rec.assignment_center_id = rec.sale_id.assignment_center_id
            else:
                rec.assignment_center_id = False
