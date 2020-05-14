# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'
    terms_sales = fields.Text(store=True, translate=True)
    included_doc = fields.Text(store=True, translate=True)
    price_condition = fields.Text(store=True, translate=True)

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    terms_sales = fields.Text(help='Default purchase terms and conditions', related='company_id.terms_sales',
                                 translate=True, readonly=False)
    included_doc = fields.Text(related='company_id.included_doc', translate=True, readonly=False)
    price_condition = fields.Text(related='company_id.price_condition', readonly=False, translate=True)

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.terms_sales = self.env.user.company_id.terms_sales if self.env.user.company_id.terms_sales else 'Default Sales terms and conditions'
        self.included_doc = self.env.user.company_id.included_doc
        self.price_condition = self.env.user.company_id.price_condition
