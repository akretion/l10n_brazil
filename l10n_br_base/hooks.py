# Copyright (C) 2019 - TODAY - Raphael Valyi Akretion
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import SUPERUSER_ID, api


def post_init_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    module = env["ir.module.module"].search([("name", "=", "l10n_br_base")])
    if module.demo:
        for partner in env["res.partner"].search([("legal_name", "=", False)]):
            partner.legal_name = partner.name
