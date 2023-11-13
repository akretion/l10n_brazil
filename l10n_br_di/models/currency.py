# Copyright (C) 2022  Renato Lima - Akretion
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class DiCurrency(models.Model):
    _name = "l10n_br_di.currency"
    _description = "DI/DUIMP Currency"

    di_id = fields.Many2one(comodel_name="l10n_br_di.di")

    currency_id = fields.Many2one(comodel_name="res.currency")

    currency_rate_id = fields.Many2one(comodel_name="res.currency.rate")

    currency_date = fields.Date(related="currency_rate_id.name")

    currency_rate = fields.Float(related="currency_rate_id.rate")
