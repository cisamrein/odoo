# -*- coding: utf-8 -*-

from odoo import models, fields, api

# class AccountInvoice(models.Model):
#     _inherit = "account.move"

class AccountInvoiceLine(models.Model):
    _inherit = "account.move.line"

    item = fields.Char(string='ITEM')
    internal_ref = fields.Char(related="product_id.default_code")
    customer_ref = fields.Char(compute='_compute_customer_ref', string="Customer Ref")
    material_origin = fields.Many2one('res.country', compute='_compute_material_origin', string="Material Origin")

    def check_item(self, product):
        return str(self.move_id.invoice_line_ids.mapped('product_id').ids.index(product)+1)

    @api.onchange('product_id')
    def _onchange_item(self):
        if self.product_id:
            self.item = self.check_item(self.product_id.id)


    @api.depends('product_id')
    def _compute_material_origin(self):
        for rec in self:
            product_supplierinfo_id = self.env['product.supplierinfo'].search([('product_tmpl_id', '=',
                                                                                rec.product_id.product_tmpl_id.id)],
                                                                              limit=1)
            rec.material_origin = product_supplierinfo_id.name.country_id.id


    @api.depends('product_id')
    def _compute_customer_ref(self):
        for rec in self:
            product_customerinfo_id = self.env['product.customer.ref'].search([('product_tmpl_id', '=',
                                                                                rec.product_id.product_tmpl_id.id)],
                                                                              limit=1, order='id DESC')
            rec.customer_ref = product_customerinfo_id.name

    def _get_computed_name(self):
        self.ensure_one()

        if not self.product_id:
            return ''

        if self.partner_id.lang:
            product = self.product_id.with_context(lang=self.partner_id.lang)
        else:
            product = self.product_id

        values = product.description_sale
        # if product.partner_ref:
        #     values = product.partner_ref
        if self.journal_id.type == 'purchase':
            if product.description_purchase:
                values = product.description_purchase
        return values
