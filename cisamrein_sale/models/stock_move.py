# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StockMoveInherit(models.Model):
    _inherit = 'stock.move'

    customer_ref = fields.Char(compute='_compute_customer_ref', string="Customer Reference")
    product_description_sale = fields.Text(related='product_id.description_sale')

    @api.depends('product_id', 'picking_id.partner_id')
    def _compute_customer_ref(self):
        for rec in self:
            customer_ref = self.env['product.customer.ref'].search([('product_tmpl_id', '=', rec.product_id.product_tmpl_id.id),
                                                                    ('partner_id', '=', rec.picking_id.partner_id.id)], limit=1)
            rec.customer_ref = customer_ref.name