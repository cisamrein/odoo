# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'
    terms_purchase = fields.Text(store=True, translate=True)


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    terms_purchase = fields.Text(help='Default purchase terms and conditions', related='company_id.terms_purchase',
                                 translate=True, readonly=False)

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.terms_purchase = self.env.user.company_id.terms_purchase if self.env.user.company_id.terms_purchase else 'Default purchase terms and conditions'
