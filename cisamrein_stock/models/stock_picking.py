# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StockPickingInherit(models.Model):
    _inherit = 'stock.picking'

    other_information = fields.Text()
    particular_information = fields.Text()

    @api.model
    def create(self, vals):
        res = super(StockPickingInherit, self).create(vals)
        old_name = res.name
        if res.picking_type_code:
            res.name = "{} - {}.041".format(old_name, res.origin)
        return res
