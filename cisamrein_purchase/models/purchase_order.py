# -*- coding: utf-8 -*-

from odoo import models, fields, api

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    notes = fields.Text(default=lambda self: self.env.user.company_id.terms_purchase, translate=True)

    signature_1 = fields.Image('Responsible Signature', help='Signature received through the portal.', copy=False, attachment=True,
                               max_width=1024, max_height=1024)

    signature_2 = fields.Image('Director Signature', help='Signature received through the portal.', copy=False, attachment=True,
                               max_width=1024, max_height=1024)
    signed_by_2 = fields.Many2one('res.users', string='Director', help='Name of the person that signed the PO')

    # signed_on_2 = fields.Datetime('Signed On', help='Date of the signature.', copy=False)

    @api.depends('order_line')
    def _compute_max_line_sequence(self):
        """Allow to know the highest sequence entered in purchase order lines.
        """
        for purchase in self:
            purchase.max_line_sequence = len(purchase.order_line)

    max_line_sequence = fields.Integer(
        string='Max sequence in lines',
        compute='_compute_max_line_sequence',
        store=True
    )

    def _reset_sequence(self):
        """ Compute the current sequence for new order_line
            by counting sequence from 1
        """
        for rec in self:
            current_sequence = 1
            for line in rec.order_line:
                line.item = str(current_sequence)
                current_sequence += 1

    def copy(self, default=None):
        return super(PurchaseOrder,
            self.with_context(keep_line_sequence=True)).copy(default)

    @api.model
    def _prepare_picking(self):
        """
        Add partner_ref in generated stock.pickin
        """
        res = super(PurchaseOrder, self)._prepare_picking()
        res['cmd_customer_ref'] = self.partner_ref
        return res


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    item = fields.Char(default="1", copy=True)
    ref_int = fields.Char(related="product_id.default_code")
    ref_supplier = fields.Char()

    @api.onchange("product_id")
    def change_item(self):
        if not self.product_id:
            self.order_id._reset_sequence()

    def _get_product_purchase_description(self, product_lang):
        self.ensure_one()
        var = ""
        if len(product_lang.mapped('seller_ids')) >= 1:
            res = product_lang.mapped('seller_ids').filtered(lambda x: x.name == self.order_id.partner_id)
            if res:
                var = res.product_code if len(res) == 1 else res[-1].product_code
        self.ref_supplier = var
        name = " "

        if product_lang.description_purchase:
            name = product_lang.description_purchase
        return name
