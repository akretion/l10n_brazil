# Copyright (C) 2022  Renato Lima - Akretion
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from lxml import etree

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class Di(models.Model):
    _name = "l10n_br_di.di"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Import Customs Declaration"

    name = fields.Char(string="Name", index=True)

    date_register = fields.Date()

    date_customs = fields.Date()

    customs_state_id = fields.Many2one(
        comodel_name="res.country.state",
        domain=[("country_id.code", "=", "BR")],
    )

    customs_location = fields.Char()

    partner_id = fields.Many2one(comodel_name="res.partner")

    partner_acquirer_id = fields.Many2one(comodel_name="res.partner")

    # TODO tem um campo na DI da NFe que informa se o importador e adquirinte tbm

    partner_importer_id = fields.Many2one(comodel_name="res.partner")

    partner_procurator_id = fields.Many2one(comodel_name="res.partner")

    currency_ids = fields.One2many(
        comodel_name="l10n_br_di.currency",
        inverse_name="di_id",
    )

    line_ids = fields.One2many(
        comodel_name="l10n_br_di.line",
        inverse_name="di_id",
    )

    company_id = fields.Many2one(
        comodel_name="res.company",
        default=lambda self: self.env["res.company"]._company_default_get("l10n_br_di.di"),
    )

    state = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("confirmed", "Confirmed"),
            ("cancelled", "Cancelled"),
            ("done", "Done"),
        ],
        default="draft",
    )

    @api.onchange("company_id")
    def _onchange_company_id(self):
        if self.company_id:
            self.partner_acquirer_id = self.company_id.partner_id
            self.partner_importer_id = self.company_id.partner_id
            self.partner_procurator_id = self.company_id.partner_id

    def action_confirm(self):
        self.write({"state": "confirmed"})

    def action_cancel(self):
        self.write({"state": "cancelled"})

    def action_done(self):
        self.write({"state": "done"})
