# -*- coding: utf-8 -*-

from odoo import models, fields, api

class AccountMove(models.Model):
    _inherit = "account.move"

    narration = fields.Text(readonly=False)
    # signature_1 = fields.Image('Responsible Signature', help='Signature received through the portal.', copy=False,
    #                            attachment=True,
    #                            max_width=1024, max_height=1024)
    #
    # signature_2 = fields.Image('Director Signature', help='Signature received through the portal.', copy=False,
    #                            attachment=True,
    #                            max_width=1024, max_height=1024)
    # signed_by_2 = fields.Many2one('res.users', string='Director', help='Name of the person that signed the PO')

    @api.onchange('partner_id')
    def _set_lang_orders(self):
        if self.partner_id.lang:
            self.narration = self.company_id.with_context(lang=self.partner_id.lang).note_invoice
        else:
            self.narration = self.company_id.note_invoice



class AccountInvoiceLine(models.Model):
    _inherit = "account.move.line"

    item = fields.Char(string='Item')
    internal_ref = fields.Char(related="product_id.default_code")
    customer_ref = fields.Char(compute='_compute_customer_ref', string="Customer Ref")
    material_origin = fields.Many2one('res.country', compute='_compute_material_origin', string="Material Origin")

    def check_item(self, product):
        return str(self.move_id.invoice_line_ids.mapped('product_id').ids.index(product) + 1)

    @api.onchange('product_id')
    def _onchange_product_id(self):
        for line in self:
            if not line.product_id or line.display_type in ('line_section', 'line_note'):
                continue
            self.item = self.check_item(self.product_id.id)

        return super(AccountInvoiceLine, self)._onchange_product_id()

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

        values = []
        if product.partner_ref:
            values.append(product.partner_ref)
        if self.journal_id.type == 'sale':
            if product.description_sale:
                values.append(product.description_sale)
        elif self.journal_id.type == 'purchase':
            if product.description_purchase:
                values.append(product.description_purchase)
        return values
