# Copyright (C) 2021 - TODAY Renato Lima - Akretion
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "Brazilian Fiscal Import content sheet",
    "summary": "Brazilian Fiscal import content sheet.",
    "category": "Localization",
    "license": "AGPL-3",
    "author": "Akretion, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/l10n-brazil",
    "version": "12.0.1.0.0",
    "depends": ["l10n_br_fiscal"],
    "data": [
        # Security
        "security/fiscal_fci.xml",
        "security/ir.model.access.csv",

        # Views
        "views/fci.xml",
        "views/fci_line.xml",
        "views/product_template.xml",
        "views/product_product.xml",

        # Actions
        "views/l10n_br_fiscal_fci_action.xml",

        # Menus
        "views/l10n_br_fiscal_fci_menu.xml",
    ],
    "installable": True,
    "development_status": "Beta",
}
