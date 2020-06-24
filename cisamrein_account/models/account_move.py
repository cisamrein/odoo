# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = "account.move"

    narration = fields.Text(readonly=False)
    arc_doc = fields.Char(compute='_set_arc_name')
    cmd_customer_ref = fields.Char(compute='_compute_cmd_customer_ref')
    assignment_center = fields.Many2one('res.partner', compute='_compute_cmd_customer_ref')

    @api.onchange('partner_id')
    def _set_lang_orders(self):
        if self.partner_id.lang:
            self.narration = self.company_id.with_context(lang=self.partner_id.lang).note_invoice
        else:
            self.narration = self.company_id.note_invoice


    @api.depends("invoice_origin")
    def _set_arc_name(self):
        if self.invoice_origin:
            self.arc_doc = "ARC - {}".format(str(self.invoice_origin).replace("/", "_"))

    @api.depends("invoice_origin")
    def _compute_cmd_customer_ref(self):
        if self.invoice_origin:
            so = self.env['sale.order'].sudo().search([("name", "=", self.invoice_origin)], limit=1)
            if so:
                self.cmd_customer_ref = so.cmd_customer_ref
                self.assignment_center = so.assignment_center


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

        values = product.description_sale
        # if product.partner_ref:
        #     values = product.partner_ref
        if self.journal_id.type == 'purchase':
            if product.description_purchase:
                values = product.description_purchase
        return values


