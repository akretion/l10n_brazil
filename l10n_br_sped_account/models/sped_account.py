# Copyright (C) 2020  Renato Lima - Akretion
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class SpedAccount(models.Model):
    _name = 'l10n_br_sped_account.account'
    _description = 'SPED Account'
    _order = 'code'

    code = fields.Char(
        string='Code',
        size=64,
        required=True,
        index=True)

    name = fields.Char(
        string='Name',
        required=True,
        index=True)

    active = fields.Boolean(
        string='Active',
        default=True)

    account_type = fields.Selection(
        selection=[
            ('A', 'Analytic'),
            ('S', 'Sintetic')],
        string='Type Account',
        required=True,
        default='A')

    sped_type = fields.Char(string='SPED Type')

    level = fields.Char(string='Account level')

    sped_table = fields.Char(string='SPED Table')

    note = fields.Text(string='Note')

    company_id = fields.Many2one(
        comodel_name='res.company',
        string='Company',
        required=True,
        default=lambda self: self.env.user.company_id)

    parent_id = fields.Many2one(
        comodel_name='l10n_br_sped_account.account',
        string="Parent Account")

    child_ids = fields.One2many(
        comodel_name='l10n_br_sped_account.account',
        inverse_name='parent_id',
        string='Children Accounts')

    account_ids = fields.One2many(
        comodel_name='account.account',
        inverse_name='sped_account_id',
        string='Account')
