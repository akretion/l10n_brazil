# Copyright (C) 2013  Renato Lima - Akretion
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "Módulo fiscal brasileiro",
    "summary": "Fiscal module/tax engine for Brazil",
    "category": "Localisation",
    "license": "AGPL-3",
    "author": "Akretion, Odoo Community Association (OCA)",
    "maintainers": ["renatonlima"],
    "website": "https://github.com/OCA/l10n-brazil",
    "development_status": "Production/Stable",
    "version": "16.0.2.11.0",
    "depends": [
        "product",
        "l10n_br_base",
    ],
    "data": [
        # Security
        "security/fiscal_security.xml",
        "security/ir.model.access.csv",

        # Data
        "data/l10n_br_fiscal_email_template.xml",
        "data/l10n_br_fiscal_data.xml",
        "data/uom_data.xml",
        "data/uom_alternative_data.xml",
        "data/product_data.xml",
        "data/partner_profile_data.xml",
        "data/res_partner_data.xml",
        "data/l10n_br_fiscal.tax.group.csv",
        "data/l10n_br_fiscal.icms.relief.csv",
        "data/l10n_br_fiscal.document.type.csv",
        "data/l10n_br_fiscal.product.genre.csv",
        "data/l10n_br_fiscal.cst.csv",
        "data/l10n_br_fiscal.tax.csv",
        "data/l10n_br_fiscal.tax.pis.cofins.csv",
        "data/l10n_br_fiscal_server_action.xml",
        "data/ir_cron.xml",
        "data/l10n_br_fiscal_comment_data.xml",

        # the following data files will be loaded as noupdate=True
        "data/l10n_br_fiscal.cnae.csv",
        "data/l10n_br_fiscal.cfop.csv",
        "data/l10n_br_fiscal_cfop_data.xml",
        "data/l10n_br_fiscal.tax.ipi.control.seal.csv",
        "data/l10n_br_fiscal.tax.ipi.guideline.csv",
        "data/l10n_br_fiscal.tax.ipi.guideline.class.csv",
        "data/l10n_br_fiscal.tax.pis.cofins.base.csv",
        "data/l10n_br_fiscal.tax.pis.cofins.credit.csv",
        "data/l10n_br_fiscal.service.type.csv",
        "data/simplified_tax_data.xml",
        "data/operation_data.xml",
        "data/l10n_br_fiscal_tax_icms_data.xml",
        "data/l10n_br_fiscal.ncm.csv",  # (partial load if demo/test)
        "data/l10n_br_fiscal.nbm.csv",  # (partial load if demo/test)
        "data/l10n_br_fiscal.nbs.csv",  # (partial load if demo/test)
        "data/l10n_br_fiscal.cest.csv", # (partial load if demo/test)

        # Views
        "views/cnae_view.xml",
        "views/cfop_view.xml",
        "views/comment_view.xml",
        "views/cst_view.xml",
        "views/tax_group_view.xml",
        "views/tax_view.xml",
        "views/tax_definition_view.xml",
        "views/icms_regulation_view.xml",
        "views/icms_relief_view.xml",
        "views/tax_pis_cofins_view.xml",
        "views/tax_pis_cofins_base_view.xml",
        "views/tax_pis_cofins_credit_view.xml",
        "views/tax_ipi_control_seal_view.xml",
        "views/tax_ipi_guideline_view.xml",
        "views/tax_ipi_guideline_class_view.xml",
        "views/ncm_view.xml",
        "views/nbm_view.xml",
        "views/nbs_view.xml",
        "views/service_type_view.xml",
        "views/cest_view.xml",
        "views/product_genre_view.xml",
        "views/document_type_view.xml",
        "views/document_serie_view.xml",
        "views/document_email_view.xml",
        "views/simplified_tax_view.xml",
        "views/simplified_tax_range_view.xml",
        "views/operation_view.xml",
        "views/operation_line_view.xml",
        "views/product_template_view.xml",
        "views/product_product_view.xml",
        "views/tax_estimate_view.xml",
        "views/partner_profile_view.xml",
        "views/res_partner_view.xml",
        "views/res_company_view.xml",
        "views/document_view.xml",
        "views/document_related_view.xml",
        "views/document_line_view.xml",
        "views/document_fiscal_line_mixin_view.xml",
        "views/res_config_settings_view.xml",
        "views/subsequent_operation_view.xml",
        "views/subsequent_document_view.xml",
        "views/uom_uom.xml",
        "views/invalidate_number_view.xml",
        "views/city_taxation_code.xml",
        "views/operation_dashboard_view.xml",

        # Actions
        "views/l10n_br_fiscal_action.xml",

        # Menus
        "views/l10n_br_fiscal_menu.xml",
    ],
    "demo": [
        "demo/city_taxation_code_demo.xml",
        "demo/company_demo.xml",
        "demo/product_demo.xml",
        "demo/partner_demo.xml",
        "demo/fiscal_document_nfse_demo.xml",
        "demo/fiscal_operation_demo.xml",
        "demo/subsequent_operation_demo.xml",
        "demo/l10n_br_fiscal_document_email.xml",
        "demo/res_users_demo.xml",
        "demo/icms_tax_definition_demo.xml",
        "demo/fiscal_document_demo.xml",
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
    "external_dependencies": {
        "python": [
            "erpbrasil.base>=2.3.0",
        ]
    },
}
