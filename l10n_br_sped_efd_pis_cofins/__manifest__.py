# Copyright 2018 Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "SPED - EFD PIS COFINS",
    "summary": """
        Registros do EFD PIS COFINS do SPED""",
    "version": "14.0.1.0.0",
    "license": "AGPL-3",
    "author": "Akretion, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/l10n-brazil",
    "development_status": "Alpha",
    "maintainers": ["rvalyi", "renatonlima"],
    "depends": ["l10n_br_sped_base", "l10n_br_account"],
    "external_dependencies": {
        "python": [
            "erpbrasil.base>=2.3.0",
        ]
    },
    "data": [
        "security/ir.model.access.csv",
        "views/sped_efd_pis_cofins.xml",
    ],
    "demo": [],
    "application": True,
    "post_init_hook": "post_init_hook",
}
