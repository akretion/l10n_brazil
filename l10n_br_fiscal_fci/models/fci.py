# Copyright (C) 2021 Renato Lima (Akretion)
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class FCI(models.Model):
    _name = "l10n_br_fiscal.fci"
    _description = "Brazilian Fiscal Import content sheet"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
        string="Name",
    )

    hash_code = fields.Char(
        string="Hash Code",
    )

    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
        default=lambda self: self.env["res.company"]._company_default_get("l10n_br_fiscal.fci")
    )

    line_ids = fields.One2many(
        comodel_name="l10n_br_fiscal.fci.line",
        inverse_name="fci_id",
        string="FCI Lines",
    )

    state = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("exported", "Exported"),
            ("imported", "Imported")],
        string="State",
        default="draft",
    )
