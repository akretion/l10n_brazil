# Copyright 2024 - TODAY Akretion - Raphael Valyi <raphael.valyi@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade

_field_renames = [
    (
        "res.partner",
        "res_partner",
        "nfe40_choice2",
        "nfe40_choice_cnpj_cpf",
    ),
    (
        "res.partner",
        "res_partner",
        "nfe40_choice6",
        "nfe40_choice_cnpj_cpf",
    ),
    (
        "res.partner",
        "res_partner",
        "nfe40_choice8",
        "nfe40_choice_cnpj_cpf",
    ),
    (
        "res.partner",
        "res_partner",
        "nfe40_choice19",
        "nfe40_choice_cnpj_cpf",
    ),
    (
        "res.partner",
        "res_partner",
        "nfe40_choice7",
        "nfe40_choice_cnpj_cpf_idest",
    ),
    (
        "res.company",
        "res_company",
        "nfe40_choice6",
        "nfe40_choice_cnpj_cpf",
    ),
    (
        "l10n_br_fiscal.document.related",
        "l10n_br_fiscal_document_related",
        "nfe40_choice4",
        "nfe40_choice_doc_type",
    ),
    (
        "l10n_br_fiscal.document.line",
        "l10n_br_fiscal_document_line",
        "nfe40_choice10",
        "nfe40_choice_icms_issqn",
    ),
    (
        "l10n_br_fiscal.document.line",
        "l10n_br_fiscal_document_line",
        "nfe40_choice10",
        "nfe40_choice_icms_issqn",
    ),
    (
        "l10n_br_fiscal.document.line",
        "l10n_br_fiscal_document_line",
        "nfe40_choice10",
        "nfe40_choice_icms_issqn",
    ),
    (
        "l10n_br_fiscal.document.line",
        "l10n_br_fiscal_document_line",
        "nfe40_choice11",
        "nfe40_choice_icms_type",
    ),
    (
        "l10n_br_fiscal.document.line",
        "l10n_br_fiscal_document_line",
        "nfe40_choice12",
        "nfe40_choice_pis_type",
    ),
    (
        "l10n_br_fiscal.document.line",
        "l10n_br_fiscal_document_line",
        "nfe40_choice13",
        "nfe40_choice_pis_trib_type",
    ),
    (
        "l10n_br_fiscal.document.line",
        "l10n_br_fiscal_document_line",
        "nfe40_choice15",
        "nfe40_choice_cofins_type",
    ),
    (
        "l10n_br_fiscal.document.line",
        "l10n_br_fiscal_document_line",
        "nfe40_choice16",
        "nfe40_choice_cofins_trib_type",
    ),
    (
        "l10n_br_fiscal.document.line",
        "l10n_br_fiscal_document_line",
        "nfe40_choice20",
        "nfe40_choice_ipi_trib_type",
    ),
]


@openupgrade.migrate(use_env=True)
def migrate(env, version):
    if not openupgrade.column_exists(env.cr, "res_partner", "nfe40_choice_cnpj_cpf"):
        openupgrade.rename_fields(env, _field_renames)
