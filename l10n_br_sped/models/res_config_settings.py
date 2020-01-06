# Copyright (C) 2020  Renato Lima - Akretion
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    module_l10n_br_sped_account = fields.Boolean(string="Use SPED Account")

    module_l10n_br_sped_fiscal = fields.Boolean(string="Use SPED Fiscal")
