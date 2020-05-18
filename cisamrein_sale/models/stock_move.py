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

    def _get_new_picking_values(self):
        res = super(StockMoveInherit, self)._get_new_picking_values()
        picking_type_id = self.env['stock.picking.type'].browse(res['picking_type_id'])
        if picking_type_id.code == 'outgoing':
            group_id = self.mapped('group_id')
            res['include_document'] = group_id.sale_id.include_document
        return res