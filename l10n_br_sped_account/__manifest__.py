# Copyright (C) 2020  Renato Lima - Akretion
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "SPED Account",
    "summary": "Brazilian Localization SPED Account.",
    "category": "Localisation",
    "license": "AGPL-3",
    "author": "Akretion, " "Odoo Community Association (OCA)",
    "website": "http://odoo-brasil.org",
    "version": "12.0.1.0.0",
    "depends": [
        "l10n_br_sped",
        "l10n_br_account",
    ],
    "data": [
        # Security
        "security/l10n_br_sped_account.xml",
        "security/ir.model.access.csv",

        # Data
        "data/l10n_br_sped_account.xml",
        "data/l10n_br_sped_account.template.csv",

        # View
        "views/sped_account_chart_template_view.xml",
        "views/sped_account_template_view.xml",
        "views/sped_account_account_view.xml",
        "views/res_partner_view.xml",
        "views/res_company_view.xml",
        "views/res_config_settings_view.xml",

        # Action
        "views/l10n_br_sped_account_action.xml",

        # Menu
        "views/l10n_br_sped_account_menu.xml",
    ],
    "demo": [
        "demo/l10n_br_sped_account.xml",
    ],
    "installable": True,
    "auto_install": False,
}
