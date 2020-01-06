# Copyright (C) 2020  Renato Lima - Akretion
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "SPED Fiscal",
    "summary": "Brazilian Localization SPED Fiscal.",
    "category": "Localisation",
    "license": "AGPL-3",
    "author": "Akretion, " "Odoo Community Association (OCA)",
    "website": "http://odoo-brasil.org",
    "version": "12.0.1.0.0",
    "depends": [
        "l10n_br_sped",
        # "l10n_br_sped_fiscal_specs"
    ],
    "data": [
        # Security
        "security/l10n_br_sped_account.xml",
        "security/ir.model.access.csv",

        # Data
        "data/l10n_br_sped_account.xml",

        # View
        "views/res_partner_view.xml",
        "views/res_company_view.xml",

        # Action
        "views/l10n_br_sped_fiscal_action.xml",

        # Menu
        "views/l10n_br_sped_fiscal_menu.xml",
    ],
    "demo": [
        "demo/l10n_br_sped_fiscal.xml",
    ],
    "installable": True,
    "auto_install": False,
}
