# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StockProductionLot(models.Model):
    _inherit = 'stock.production.lot'

    def name_get(self):
        return [(lot.id, "%s(%s)" % (lot.name, lot.product_id.name) or _('Draft Payment')) for lot in self]