# Copyright (C) 2021  Renato Lima - Akretion <renato.lima@akretion.com.br>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class DocumentServiceMessage(models.Model):
    _name = "l10n_br_fiscal.document.service.message"
    _inherit = "l10n_br_fiscal.data.abstract"
    _description = "Generic Document Service Message"

    name = fields.Char(string="Name", required=True, index=True)

    description = fields.Text(string="Description", required=True, index=True)

    document_type_id = fields.Many2one(
        comodel_name="l10n_br_fiscal.document.type",
        string="Fiscal Document Type",
    )

    document_service_id = fields.Many2one(
        comodel_name="l10n_br_fiscal.document.service",
        string="Fiscal Document Service",
    )
