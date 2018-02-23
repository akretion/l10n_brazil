# -*- coding: utf-8 -*-
# Copyright (C) 2013  Renato Lima - Akretion
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    'name': 'Brazilian Localization Account Product',
    'summary': "Brazilian Localization Account Product",
    'category': 'Localisation',
    'license': 'AGPL-3',
    'author': 'Akretion, Odoo Community Association (OCA)',
    'website': 'http://odoo-brasil.org',
    'version': '8.0.3.0.0',
    'depends': [
        'l10n_br_data_account',
        'account_product_fiscal_classification',
    ],
    'data': [
        'l10n_br_account_product_sequence.xml',
        'account_invoice_workflow.xml',
        'data/l10n_br_account_product.cfop.csv',
        'data/l10n_br_account.fiscal.document.csv',
        'data/l10n_br_account_data.xml',
        'data/l10n_br_account_product_data.xml',
        'data/l10n_br_tax.icms_partition.csv',
        'data/ir_cron.xml',
        'views/l10n_br_account_product_view.xml',
        'views/l10n_br_account_view.xml',
        'views/l10n_br_account_product_cfop_view.xml',
        'views/l10n_br_account_service_type_view.xml',
        'views/l10n_br_account_product_ipi_guideline_view.xml',
        'views/l10n_br_account_product_icms_relief_view.xml',
        'views/l10n_br_account_product_import_declaration_view.xml',
        'views/account_tax_template_view.xml',
        'views/account_view.xml',
        'views/account_invoice_view.xml',
        'wizard/l10n_br_account_invoice_costs_ratio_view.xml',
        'views/nfe/account_invoice_nfe_view.xml',
        'views/res_partner_view.xml',
        'views/res_company_view.xml',
        'views/account_product_fiscal_classification_template_view.xml',
        'views/account_product_fiscal_classification_view.xml',
        'views/product_view.xml',
        'views/res_country_view.xml',
        'wizard/l10n_br_account_nfe_export_invoice_view.xml',
        'wizard/l10n_br_account_nfe_export_view.xml',
        'wizard/l10n_br_account_document_status_sefaz_view.xml',
        'wizard/account_invoice_refund_view.xml',
        'security/l10n_br_account_product_security.xml',
        'security/ir.model.access.csv',
        'report/account_invoice_report_view.xml',
    ],
    'demo': [
        'demo/account_tax_code_demo.xml',
        'demo/account_tax_demo.xml',
        'demo/base_demo.xml',
        'demo/product_demo.xml',
        'demo/l10n_br_account_product_demo.xml',
        'demo/account_fiscal_position_rule_demo.xml',
        'demo/product_taxes.yml',
    ],
    'test': [
        'test/account_customer_invoice.yml',
        'test/account_supplier_invoice.yml',
        'test/account_invoice_refund.yml',
        'test/nfe_export.yml',
    ],
    'installable': False,
    'auto_install': False,
}
