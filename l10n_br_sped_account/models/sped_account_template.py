# Copyright (C) 2020  Renato Lima - Akretion
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class SpedAccountTemplate(models.Model):
    _name = 'l10n_br_sped_account.template'
    _description = 'SPED Account Template'
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

    account_type = fields.Selection(
        selection=[
            ('A', 'Analytic'),
            ('S', 'Sintetic')],
        string='Type Account',
        required=True,
        default='A')

    nocreate = fields.Boolean(
        string='Optional Create',
        default=False,
        help="If checked, the new chart of accounts"
             " will not contain this by default.")

    sped_type = fields.Char(string='SPED Type')

    level = fields.Char(string='Account level')

    sped_table = fields.Char(string='SPED Table')

    note = fields.Text(string='Note')

    parent_id = fields.Many2one(
        comodel_name='l10n_br_sped_account.template',
        string="Parent Account")

    sped_chart_template_id = fields.Many2one(
        comodel_name='l10n_br_sped_account.chart.template',
        string='SPED Chart Template',
        help="This optional field allow you to link an fiscal account "
             "template to a specific fiscal chart template that may differ "
             "from the one its root parent belongs to.")
