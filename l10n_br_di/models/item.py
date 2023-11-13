# Copyright (C) 2022  Renato Lima - Akretion
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

from ...l10n_br_fiscal.constants.fiscal import (
    FINAL_CUSTOMER,
    FINAL_CUSTOMER_YES
)


class DiItem(models.Model):
    _name = "l10n_br_di.item"
    _inherit = "l10n_br_fiscal.document.line.mixin"
    _description = "Import Customs Declaration Item"
    _order = "item_sequence ASC"

    name = fields.Text()

    item_sequence = fields.Char()

    line_origin = fields.Selection(
        selection=[
            ("product", "From Products"),
            ("purchase_receipts", "From Purchase Receipts"),
        ],
        string="Origin Line",
        default="product",
    )

    line_id = fields.Many2one(comodel_name="l10n_br_di.line")

    line_number = fields.Char(related="line_id.line_number")

    tax_framework = fields.Selection(
        related="line_id.di_id.company_id.tax_framework",
    )

    partner_id = fields.Many2one(related="line_id.di_id.partner_id")

    ind_final = fields.Selection(
        selection=FINAL_CUSTOMER,
        string="Final Consumption Operation",
        default=FINAL_CUSTOMER_YES,
    )

    company_id = fields.Many2one(related="line_id.di_id.company_id")
