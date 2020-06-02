# -*- coding: utf-8 -*-

from odoo import models, fields, api

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    notes = fields.Text(readonly=False)

    signature_1 = fields.Image('Responsible Signature', help='Signature received through the portal.', copy=False, attachment=True,
                               max_width=1024, max_height=1024)

    signature_2 = fields.Image('Director Signature', help='Signature received through the portal.', copy=False, attachment=True,
                               max_width=1024, max_height=1024)
    signed_by_2 = fields.Many2one('res.users', string='Director', help='Name of the person that signed the PO')

    # signed_on_2 = fields.Datetime('Signed On', help='Date of the signature.', copy=False)

    @api.onchange('partner_id')
    def _set_lang_orders(self):
        if self.partner_id.lang:
            self.notes = self.env.user.company_id.with_context(lang=self.partner_id.lang).terms_purchase
        else:
            self.notes = self.env.user.company_id.terms_purchase

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

    def _prepare_stock_moves(self, picking):
        """ Prepare the stock moves data for one order line. This function returns a list of
        dictionary ready to be used in stock.move's create()
        """
        self.ensure_one()
        res = []
        if self.product_id.type not in ['product', 'consu']:
            return res
        qty = 0.0
        price_unit = self._get_stock_move_price_unit()
        for move in self.move_ids.filtered(lambda x: x.state != 'cancel' and not x.location_dest_id.usage == "supplier"):
            qty += move.product_uom._compute_quantity(move.product_uom_qty, self.product_uom, rounding_method='HALF-UP')
        template = {
            # truncate to 2000 to avoid triggering index limit error
            # TODO: remove index in master?
            'item': self.item,
            'ref_supplier':self.ref_supplier,
            'name': (self.name or '')[:2000],
            'product_id': self.product_id.id,
            'product_uom': self.product_uom.id,
            'date': self.order_id.date_order,
            'date_expected': self.date_planned,
            'location_id': self.order_id.partner_id.property_stock_supplier.id,
            'location_dest_id': self.order_id._get_destination_location(),
            'picking_id': picking.id,
            'partner_id': self.order_id.dest_address_id.id,
            'move_dest_ids': [(4, x) for x in self.move_dest_ids.ids],
            'state': 'draft',
            'purchase_line_id': self.id,
            'company_id': self.order_id.company_id.id,
            'price_unit': price_unit,
            'picking_type_id': self.order_id.picking_type_id.id,
            'group_id': self.order_id.group_id.id,
            'origin': self.order_id.name,
            'propagate_date': self.propagate_date,
            'propagate_date_minimum_delta': self.propagate_date_minimum_delta,
            'description_picking': self.product_id._get_description(self.order_id.picking_type_id),
            'propagate_cancel': self.propagate_cancel,
            'route_ids': self.order_id.picking_type_id.warehouse_id and [(6, 0, [x.id for x in self.order_id.picking_type_id.warehouse_id.route_ids])] or [],
            'warehouse_id': self.order_id.picking_type_id.warehouse_id.id,
        }
        diff_quantity = self.product_qty - qty
        if float_compare(diff_quantity, 0.0,  precision_rounding=self.product_uom.rounding) > 0:
            po_line_uom = self.product_uom
            quant_uom = self.product_id.uom_id
            product_uom_qty, product_uom = po_line_uom._adjust_uom_quantities(diff_quantity, quant_uom)
            template['product_uom_qty'] = product_uom_qty
            template['product_uom'] = product_uom.id
            res.append(template)
        return res
