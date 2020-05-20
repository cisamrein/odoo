# -*- coding: utf-8 -*-

from odoo import models, fields, api

class StockRuleInherit(models.Model):
    _inherit = 'stock.rule'

    def _get_custom_move_fields(self):
        fields = super(StockRuleInherit, self)._get_custom_move_fields()
        fields += ['item']
        return fields