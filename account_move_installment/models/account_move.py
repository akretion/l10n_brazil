# Copyright (C) 2021 - TODAY Renato Lima - Akretion
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    receivable_line_ids = fields.Many2many(
        comodel_name="account.move.line",
        compute="_compute_receivable_line_ids",
        store=True,
        string="Receivable Move Lines",
    )

    payable_line_ids = fields.Many2many(
        "account.move.line",
        string="Payable Move Lines",
        compute="_compute_payable_line_ids",
        store=True,
    )

    @api.depends("line_ids", "state")
    def _compute_receivable_line_ids(self):
        for move in self:
            lines = move.line_ids.filtered(
                lambda line: line.account_id.account_type
                in ("asset_receivable", "liability_payable")
            )
            move.receivable_line_ids = lines.sorted()

    @api.depends("line_ids.amount_residual")
    def _compute_payable_line_ids(self):
        for move in self:
            (
                invoice_partials,
                exchange_diff_moves,
            ) = move._get_reconciled_invoices_partials()
            move.payable_line_ids = [partial[2].id for partial in invoice_partials]
