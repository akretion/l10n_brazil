# Copyright (C) 2022  Renato Lima - Akretion
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "Brazilian Import Customs Declaration",
    "summary": "Brazilian Import Customs Declaration (DI/DUIMP).",
    "category": "Localisation",
    "license": "AGPL-3",
    "author": "Akretion, Odoo Community Association (OCA)",
    "maintainers": ["renatonlima"],
    "website": "https://github.com/OCA/l10n-brazil",
    "version": "12.0.1.0.0",
    "development_status": "Production/Stable",
    "depends": [
        "l10n_br_fiscal",
    ],
    "data": [
        # security
        "security/l10n_br_di_security.xml",
        "security/ir.model.access.csv",
        # Data

        # Views
        "views/di_view.xml",
        "views/line_view.xml",
        "views/item_view.xml",
        # Wizards
        # "wizards/document_cancel_wizard.xml",
        # Actions
        "views/l10n_br_di_action.xml",
        # Menus
        "views/l10n_br_di_menu.xml",
    ],
    "installable": True,
    "auto_install": False,
}
