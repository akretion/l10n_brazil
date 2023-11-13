# Copyright (C) 2022  Renato Lima - Akretion
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class DiItem(models.Model):
    _inherit = "l10n_br_di.item"

    line_origin = fields.Selection(
        default="purchase_receipts",
    )

    purchase_line_ids = fields.Many2one(
        comodel_name="purchase.order.line",
    )

    @api.onchange("purchase_line_ids")
    def _onchange_purchase_line_ids(self):
        if self.purchase_line_ids:
            self.product_id = self.purchase_line_ids.product_id
            self.name = self.purchase_line_ids.name
            self.price_unit = self.purchase_line_ids.price_unit
            self.quantity = self.purchase_line_ids.quantity
            self.fiscal_operation_id = self.purchase_line_ids.company_id.purchase_fiscal_operation_id
        else:
            self.product_id = False
            self.name = False
            self.price_unit = 0.0
            self.quantity = 0.0
