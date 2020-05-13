# -*- coding: utf-8 -*-

from odoo import models, fields, api

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    notes = fields.Text(default=lambda self: self.env.user.company_id.terms_purchase, translate=True)

    signature_1 = fields.Image('Signature', help='Signature received through the portal.', copy=False, attachment=True,
                               max_width=1024, max_height=1024)
    signed_by_1 = fields.Many2one('res.users', string='Responsible', help='Name of the person that signed the PO')
    # signed_on_1 = fields.Datetime('Signed On', help='Date of the signature.', copy=False)

    signature_2 = fields.Image('Signature', help='Signature received through the portal.', copy=False, attachment=True,
                               max_width=1024, max_height=1024)
    signed_by_2 = fields.Many2one('res.users', string='Director', help='Name of the person that signed the PO.')

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
                line.item = current_sequence
                current_sequence += 1

    def copy(self, default=None):
        return super(PurchaseOrder,
            self.with_context(keep_line_sequence=True)).copy(default)


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    item = fields.Integer(default=0, copy=True)

    @api.onchange("product_id")
    def change_item(self):
        if not self.product_id:
            self.order_id._reset_sequence()
