# Copyright (C) 2021  Magno Costa - Akretion
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def _get_partner_to_invoice(self):
        self.ensure_one()
        partner = self.partner_id
        if self.sale_id:
            partner = self.sale_id.partner_invoice_id
        return partner.address_get(["invoice"]).get("invoice")

    def write(self, values):
        # Forma encontrada para evitar que Operação Fiscal do metodo default
        # seja preenchida quando o Pedido não tem o campo preenchido
        if self.sale_id:
            if not self.sale_id.fiscal_operation_id:
                values["fiscal_operation_id"] = False

        return super().write(values)
