# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StockPickingInherit(models.Model):
    _inherit = 'stock.picking'

    other_information = fields.Text()
    particular_information = fields.Text()

    @api.model
    def create(self, vals):
        res = super(StockPickingInherit, self).create(vals)
        if self.env['sale.order'].search([('name', '=', self.origin)]):
            old_name = self.name
            if self.picking_type_id.code == 'PICK':
                self.name = "PICK_{}/{}.041".format(old_name, self.origin)
            elif self.picking_type_id.code == 'PACK':
                self.name = "PACK_{}/{}.041".format(old_name, self.origin)
            else:
                self.name = "{}/{}.041".format(old_name, self.origin)
        return res
