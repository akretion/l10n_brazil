# Copyright (C) 2021 Renato Lima (Akretion)
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class FCILine(models.Model):
    _name = "l10n_br_fiscal.fci.line"
    _description = "Brazilian Fiscal Import content sheet Line"
    _rec_name = "hash_code"

    fci_id = fields.Many2one(
        comodel_name="l10n_br_fiscal.fci",
    )

    product_tmpl_id = fields.Many2one(
        comodel_name="product.template",
        string="Product Template",
    )

    product_id = fields.Many2one(
        comodel_name="product.product",
        string="Product Variant",
    )

    hash_code = fields.Char(
        string="Hash Code",
    )

    import_content_percent = fields.Float(
        string="Import Content %",
    )
