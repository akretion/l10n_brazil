# Copyright (C) 2021 Renato Lima (Akretion)
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    fci_id = fields.Many2one(
        comodel_name="l10n_br_fiscal.fci.line",
        company_dependent=True,
        string="FCI",
        help="Current FCI used by variant",
    )
