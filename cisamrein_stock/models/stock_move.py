# -*- coding: utf-8 -*-

from odoo import models, fields, api

class StockMoveInherit(models.Model):
    _inherit = 'stock.move'

    item = fields.Char()
    product_description = fields.Text(related='product_id.description_sale')
    product_default_code = fields.Char(related='product_id.default_code', string="Internal Reference")
    material_origin = fields.Many2one('res.country', compute='_compute_material_origin')
    ref_supplier = fields.Char()

    @api.depends('product_id')
    def _compute_material_origin(self):
        for rec in self:
            product_supplierinfo_id = self.env['product.supplierinfo'].search([('product_tmpl_id', '=',
                                                                                 rec.product_id.product_tmpl_id.id)], limit=1)
            rec.material_origin = product_supplierinfo_id.name.country_id.id

    @api.model
    def create(self, values):
        # Add code here
        res = super(StockMoveInherit, self).create(values)
        if res.purchase_line_id:
            res.item = res.purchase_line_id.item
            res.ref_supplier = res.purchase_line_id.ref_supplier
        return res