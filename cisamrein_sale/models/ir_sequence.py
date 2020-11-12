# -*- coding: utf-8 -*-

from odoo import models, api


class IrSequence(models.Model):
    _inherit = 'ir.sequence'

    @api.model
    def update_sequence_order(self):
        so_seq = self.search([('code', '=', 'sale.order')], limit=1)
        if so_seq:
           so_seq.prefix = so_seq.prefix.replace("SO/", "Offre/Offer-")

        sp_seq = self.search([('prefix', '=', 'WH/OUT/')], limit=1)
        if sp_seq:
            sp_seq.prefix = sp_seq.prefix.replace("WH/OUT/", "N°")
