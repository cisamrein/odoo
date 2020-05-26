# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ResCompany(models.Model):
    _inherit = "res.company"
    note_invoice = fields.Text(default='Invoice general terms', translate=True, store=True)

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    note_invoice = fields.Text(related='company_id.note_invoice', translate=True, readonly=False)

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.note_invoice = self.env.user.company_id.note_invoice