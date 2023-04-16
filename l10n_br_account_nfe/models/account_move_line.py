# Copyright (C) 2022-Today - Akretion (<https://akretion.com/pt-BR>).
# @author Renato Lima <renato.lima@akretion.com.br>
# Copyright (C) 2023-Today Raphaël Valyi <raphael.valyi@akretion.com.br> - Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import string
from odoo import api, models, fields
from odoo.addons.spec_driven_model.models import spec_models



from odoo.addons.l10n_br_fiscal.constants.fiscal import (
    DOCUMENT_ISSUER_COMPANY,
    MODELO_FISCAL_NFCE,
    MODELO_FISCAL_NFE,
    PROCESSADOR_OCA,
    SITUACAO_EDOC_A_ENVIAR,
)


class AccountMoveLine(models.Model):
    _inherit = ["account.move.line", "spec.mixin"]
    _name = "account.move.line"
#    _inherit = "account.move.line"

    _field_prefix = "nfe40_"
    _schema_name = "nfe"
    _schema_version = "4.0.0"
    _odoo_module = "l10n_br_account_nfe"
    _spec_module = "odoo.addons.l10n_br_nfe_spec.models.v4_0.leiaute_nfe_v4_00"
    _spec_tab_name = "NFe"
#    _nfe_search_keys = ["nfe40_Id"]

    def get_concrete_model(self, comodel_name):
        comodel = super().get_concrete_model(comodel_name)
        if comodel == self.env["l10n_br_fiscal.document.line"]:
            return self.env["account.move.line"]
        return comodel

    def _build_string_not_simple_type(self, key, vals, value, node):
        # if key not in ["nfe40_CST", "nfe40_modBC", "nfe40_CSOSN", "nfe40_vBC"]:
        if key not in ["nfe40_CST", "nfe40_modBC", "nfe40_CSOSN"]:
            return super()._build_string_not_simple_type(key, vals, value, node)
            # TODO avoid collision with cls prefix
        elif key == "nfe40_CST":
            if str(type(node)).startswith("Tnfe.InfNfe.Det.Imposto.Icms"):
                vals["icms_cst_id"] = (
                    self.env["l10n_br_fiscal.cst"]
                    .search([("code", "=", value), ("tax_domain", "=", "icms")])[0]
                    .id
                )
            elif str(type(node)).startswith("Tnfe.InfNfe.Det.Imposto.Ipi"):
                vals["ipi_cst_id"] = (
                    self.env["l10n_br_fiscal.cst"]
                    .search([("code", "=", value), ("tax_domain", "=", "ipi")])[0]
                    .id
                )
            elif str(type(node)).startswith("Tnfe.InfNfe.Det.Imposto.Pis"):
                vals["pis_cst_id"] = (
                    self.env["l10n_br_fiscal.cst"]
                    .search([("code", "=", value), ("tax_domain", "=", "pis")])[0]
                    .id
                )
            elif str(type(node)).startswith("Tnfe.InfNfe.Det.Imposto.Cofins"):
                vals["cofins_cst_id"] = (
                    self.env["l10n_br_fiscal.cst"]
                    .search([("code", "=", value), ("tax_domain", "=", "cofins")])[0]
                    .id
                )
        elif key == "nfe40_modBC":
            vals["icms_base_type"] = value


    def write(self, values):
        result = super().write(values)
        MOVE_LINE_FIELDS = ["date_maturity", "name", "amount_currency"]
        if any(field in values.keys() for field in MOVE_LINE_FIELDS):
            invoices = self.mapped("move_id")
            for invoice in invoices.filtered(
                lambda i: i.fiscal_document_id.id != i.company_id.fiscal_dummy_id.id
                and i.processador_edoc == PROCESSADOR_OCA
                and i.document_type_id.code in [MODELO_FISCAL_NFE, MODELO_FISCAL_NFCE]
                and i.issuer == DOCUMENT_ISSUER_COMPANY
                and i.state_edoc == SITUACAO_EDOC_A_ENVIAR
            ):
                invoice.fiscal_document_id.action_document_confirm()
                invoice.fiscal_document_id._document_export()
        return result
