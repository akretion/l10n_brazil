# Copyright (C) 2022  Renato Lima - Akretion
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class DiLine(models.Model):
    _name = "l10n_br_di.line"
    _description = "Import Customs Declaration Line"
    _order = "line_number ASC"

    name = fields.Char()

    line_number = fields.Char()

    description = fields.Text()

    manufacturer_id = fields.Many2one(comodel_name="res.partner")

    country_origin_id = fields.Many2one(comodel_name="res.country")

    di_id = fields.Many2one(comodel_name="l10n_br_di.di")

    item_ids = fields.One2many(
        comodel_name="l10n_br_di.item",
        inverse_name="line_id"
    )

    @api.onchange("manufacturer_id")
    def _onchange_manufacturer_id(self):
        if self.manufacturer_id:
            self.country_origin_id = self.manufacturer_id.country_id
        else:
            self.country_origin_id = False
