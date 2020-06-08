# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    include_document = fields.Text(readonly=False)
    note = fields.Text(readonly=False)
    price_condition = fields.Text(readonly=False)
    cmd_customer_ref = fields.Char()
    signature_2 = fields.Image('Responsible Signature', help='Signature received through the portal.', copy=False, attachment=True,
                               max_width=1024, max_height=1024)
    signed_by_2 = fields.Many2one('res.users', string='Manager', help='Name of the person that signed the SO')
    assignment_center = fields.Many2one("res.partner", help="Add Assignment center on the Order")

    @api.onchange('partner_id')
    def _set_lang_orders(self):
        if self.partner_id.lang:
            self.include_document = self.company_id.with_context(lang=self.partner_id.lang).included_doc
            self.note = self.company_id.with_context(lang=self.partner_id.lang).terms_sales
            self.price_condition = self.company_id.with_context(lang=self.partner_id.lang).price_condition
        else:
            self.include_document = self.company_id.included_doc
            self.note = self.company_id.terms_sales
            self.price_condition = self.company_id.price_condition

    def _reset_sequence(self):
        """ Compute the current sequence for new order_line
            by counting sequence from 1
        """
        for rec in self:
            current_sequence = 1
            for line in rec.order_line:
                line.item = str(current_sequence)
                current_sequence += 1

    def print_arc_document(self):
        return self.env.ref('cisamrein_sale.arc_doc').report_action(self)

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    item = fields.Char(default="1", copy=True)
    customer_reference = fields.Char()
    ref_int = fields.Char(related="product_id.default_code")


    @api.onchange("product_id")
    def change_item(self):
        if not self.product_id:
            self.order_id._reset_sequence()

    def get_sale_order_line_multiline_description_sale(self, product):
        """ Custom name as product sale description and customer reference
        """
        var = ""
        if len(product.mapped('customer_reference_ids')) >= 1:
            res = product.mapped('customer_reference_ids').filtered(lambda x: x.partner_id.id == self.order_id.partner_id.id)
            if res:
                var = res.name if len(res) == 1 else res[-1].name

        self.customer_reference = var
        return product.get_product_multiline_description_sale()

    def _prepare_procurement_values(self, group_id=False):
        """
        Add item into values to pass
        :return:
        """
        values = super(SaleOrderLine, self)._prepare_procurement_values(group_id)
        self.ensure_one()
        values['item'] = self.item
        return values

    def _prepare_invoice_line(self):
        """
        Prepare the dict of values to create the new invoice line for a sales order line.
        """
        res = super(SaleOrderLine, self)._prepare_invoice_line()
        if self.item:
            res['item'] = self.item
        return res
