# Copyright (C) 2020  Renato Lima - Akretion
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class AccountAccount(models.Model):
    _inherit = 'account.account'

    sped_account_id = fields.Many2one(
        comodel_name='l10n_br_sped_account.account',
        string='SPED Account')
