# Copyright (C) 2022  Renato Lima - Akretion
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "Integração de Compras com a Declaração de Importação",
    "summary": "Brazilian foreign trade purchase.",
    "category": "Localisation",
    "license": "AGPL-3",
    "author": "Akretion, Odoo Community Association (OCA)",
    "maintainers": ["renatonlima"],
    "website": "https://github.com/OCA/l10n-brazil",
    "version": "12.0.1.0.0",
    "development_status": "Production/Stable",
    "depends": [
        "l10n_br_di",
        "l10n_br_purchase",
    ],
    "data": [
        # security
        # TODO "security/ir.model.access.csv",
        # Data

        # Views
        # "views/import_customs_declaration_view.xml",
        "views/import_customs_declaration_item_view.xml",
        # Wizards
        # "wizards/document_cancel_wizard.xml",
    ],
    "installable": True,
    "auto_install": True,
}
