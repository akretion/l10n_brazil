# Copyright (C) 2021 Renato Lima (Akretion)
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models, api


class ProductTemplate(models.Model):
    _inherit = "product.template"

    fci_id = fields.Many2one(
        comodel_name="l10n_br_fiscal.fci.line",
        string='FCI',
        compute='_compute_fci',
        inverse='_set_fci',
        search='_search_fci',
        help="Currency FCI used by product and variants"
    )

    @api.depends('product_variant_ids', 'product_variant_ids.fci_id')
    def _compute_fci(self):
        unique_variants = self.filtered(lambda template: len(template.product_variant_ids) == 1)
        for template in unique_variants:
            template.fci_id = template.product_variant_ids.fci_id.id
        for template in (self - unique_variants):
            template.fci_id = False

    @api.one
    def _set_fci(self):
        if len(self.product_variant_ids) == 1:
            self.product_variant_ids.fci_id = self.fci_id.id

    def _search_fci(self, operator, value):
        products = self.env['product.product'].search([('fci_id', operator, value)], limit=None)
        return [('id', 'in', products.mapped('product_tmpl_id').ids)]
