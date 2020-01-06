# Copyright (C) 2020  Renato Lima - Akretion
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class Company(models.Model):
    _inherit = "res.company"

    sped_chart_template_id = fields.Many2one(
        comodel_name='l10n_br_sped_account.chart.template',
        string='SPED Chart of Account Template',
        help='The SPED chart of account template for the company (if any)')
