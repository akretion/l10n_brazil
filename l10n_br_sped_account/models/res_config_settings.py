# Copyright (C) 2020  Renato Lima - Akretion
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    has_sped_chart_of_accounts = fields.Boolean(
        compute='_compute_has_sped_chart_of_accounts',
        string='Company has a SPED chart of accounts')

    sped_chart_template_id = fields.Many2one(
        comodel_name='l10n_br_sped_account.chart.template',
        string='SPED Chart of Account Template')

    @api.depends('company_id')
    def _compute_has_sped_chart_of_accounts(self):
        self.has_sped_chart_of_accounts = bool(
            self.company_id.sped_chart_template_id)
        self.sped_chart_template_id = (
            self.company_id.sped_chart_template_id or False)

    @api.multi
    def set_values(self):
        super(ResConfigSettings, self).set_values()
        """install a sped chart of accounts for the given company"""
        if (self.sped_chart_template_id and
                self.sped_chart_template_id !=
                    self.company_id.sped_chart_template_id):
            self.sped_chart_template_id.load_for_current_company()
