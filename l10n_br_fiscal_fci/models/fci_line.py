# Copyright (C) 2021 Renato Lima (Akretion)
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models
from odoo.addons import decimal_precision as dp


class FCILine(models.Model):
    _name = "l10n_br_fiscal.fci.line"
    _description = "Brazilian Fiscal Import Content Sheet Line"
    _rec_name = "hash_code"

    fci_id = fields.Many2one(
        comodel_name="l10n_br_fiscal.fci",
        string="FCI File",
    )

    product_tmpl_id = fields.Many2one(
        comodel_name="product.template",
        string="Product Template",
    )

    product_id = fields.Many2one(
        comodel_name="product.product",
        string="Product Variant",
    )

    name = fields.Char(
        string="Product Description",
    )

    tag_name = fields.Char(
        string="Product Tag",
    )

    hash_code = fields.Char(
        string="FCI",
    )

    company_id = fields.Many2one(
        related="fci_id.company_id",
        string="Company",
        store=True
    )

    amount_total_outgoing = fields.Float(
        string="Amount Total Outgoing",
        digits=dp.get_precision("Product Price"),
        help="Value of product with taxes.",
    )

    amount_total_imported = fields.Float(
        string="Part of Amount Total Imported",
        digits=dp.get_precision("Product Price"),
    )

    import_content_percent = fields.Float(
        string="Import Content %",
    )

    uom_id = fields.Many2one(
        comodel_name="uom.uom",
        string="UOM",
    )

    ncm_code = fields.Char(
        string="NCM",
    )

    gtin_code = fields.Char(
        string="GTIN",
    )

    product_ids = fields.One2many(
        comodel_name="product.product",
        inverse_name="fci_id",
        string="FCI Products",
    )

    def name_get(self):
        return [(r.id, "(%s) %s" % (r.name, r.hash_code)) for r in self]

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        args = list(args or [])
        if not name == "":
            args += ['|', '|', ('name', operator, name), ('tag_name', operator, name), ('hash_code', operator, name)]
        ids = self.search(args, limit=limit)
        return ids.name_get()