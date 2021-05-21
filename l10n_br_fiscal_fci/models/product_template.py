# Copyright (C) 2021 Renato Lima (Akretion)
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    fci_id = fields.Many2one(
        comodel_name="l10n_br_fiscal.fci.line",
        company_dependent=True,
        string="FCI",
        help="Currency FCI used by product and variants",
    )
