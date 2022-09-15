# Copyright 2022 Engenere
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import _, fields, models, api


class CNABReturnEvent(models.Model):

    _inherit = "l10n_br_cnab.return.event"

    ### BASE FIELDS ###

    occurrence_code_1 = fields.Char()
    occurrence_code_2 = fields.Char()
    occurrence_code_3 = fields.Char()
    occurrence_code_4 = fields.Char()
    occurrence_code_5 = fields.Char()
    bank_code = fields.Char()
    batch_code = fields.Char()
    record_type = fields.Char()
    seq_number = fields.Char()
    move_type_code = fields.Char()
    beneficiary_bank_code = fields.Char()
    # código da câmera centralizadora
    centralizing_chamber_code = fields.Char()
    beneficiary_bank_branch = fields.Char()
    beneficiary_name = fields.Char()
    beneficiary_document = fields.Char(
        helps="Beneficiary's document number, it can be a CNPJ or CPF."
    )
    beneficiary_bank_account = fields.Char()
    beneficiary_bank_account_dac = fields.Char()
    beneficiary_notification = fields.Char()
    expected_payment_date = fields.Date()
    additional_info = fields.Char()
    ted_purpose = fields.Char()
    doc_purpose = fields.Char()

    liquidation_move = fields.Boolean(
        string="Liquidation Move",
        help="If check, this CNAB Event will generate a liquidity move line.",
    )

    cnab_structure_id = fields.Many2one(
        comodel_name="l10n_br_cnab.structure",
        related="cnab_return_log_id.cnab_structure_id",
    )

    balance = fields.Float(
        compute="_compute_balance",
        help="Balance = Payment Value + Discount Value + Rebate Value - Fees",
    )

    move_line_ids = fields.Many2many(
        comodel_name="account.move.line", ondelete="restrict"
    )
    journal_id = fields.Many2one(
        comodel_name="account.journal", related="cnab_return_log_id.journal_id"
    )

    @api.depends(
        "liquidation_move",
        "payment_value",
        "discount_value",
        "rebate_value",
        "interest_fee_value",
    )
    def _compute_balance(self):
        for record in self:
            if record.liquidation_move:
                record.balance = (
                    record.payment_value
                    + record.discount_value
                    + record.rebate_value
                    - record.interest_fee_value
                )
            else:
                record.balance = 0

    @api.model
    def create(self, vals):
        """Override Create Method"""
        event = super().create(vals)
        if not event.cnab_return_log_id.cnab_structure_id:
            # if there is no cnab_structure_id it is because the return file is not being
            # processed by this module, so there is nothing to do here.
            return event
        event.load_bank_payment_line()
        event.load_description_occurrences()
        event.check_liquidation_move()
        event.set_move_line_ids()
        event.set_occurrence_date()
        return event

    def set_occurrence_date(self):
        if not self.occurrence_date:
            self.occurrence_date = self.cnab_return_log_id.cnab_date_file

    def set_move_line_ids(self):
        payment_lines = self.bank_payment_line_id.payment_line_ids
        for payment_line in payment_lines:
            self.move_line_ids = [(4, payment_line.move_line_id.id)]

    def check_liquidation_move(self):
        codes = [
            self.occurrence_code_1,
            self.occurrence_code_2,
            self.occurrence_code_3,
            self.occurrence_code_4,
            self.occurrence_code_5,
        ]
        occurrence_obj = self.env["cnab.occurrence"]

        self.liquidation_move = False
        for code in codes:
            occurrence_id = occurrence_obj.search(
                [
                    ("cnab_structure_id", "=", self.cnab_structure_id.id),
                    ("code", "=", code),
                ]
            )
            if occurrence_id.liquidation_move:
                self.liquidation_move = True

    def load_bank_payment_line(self):
        """
        When for cnab outbound payment processed by this module the
        bank_payment_line_id is filled based on your_number field
        """
        for event in self:
            if event.cnab_return_log_id.type == "outbound":
                bank_payment_line_id = self.env["bank.payment.line"].search(
                    [("name", "=", event.your_number)]
                )
                event.bank_payment_line_id = bank_payment_line_id

    def get_description_occurrence(self, event_code):
        """Get occurrence description by occurrence code"""
        occurrence_id = (
            self.cnab_return_log_id.cnab_structure_id.cnab_occurrence_ids.filtered(
                lambda a: a.code == event_code
            )
        )
        if occurrence_id:
            description = occurrence_id.name
        else:
            description = event_code + "-" + "DESCRIPTION CODE NOT FOUND"
        return description

    def load_description_occurrences(self):
        """Generate occurrence description for all occurrences"""
        for event in self:
            occurrences = ""
            event_codes = (
                event.occurrence_code_1,
                event.occurrence_code_2,
                event.occurrence_code_3,
                event.occurrence_code_4,
                event.occurrence_code_5,
            )
            for code in event_codes:
                if not code:
                    continue
                occurrences += event.get_description_occurrence(code)
            event.occurrences = occurrences

    def _get_move_vals(self):
        return {
            "name": f"CNAB Return {self.cnab_return_log_id.bank_id.short_name} - {self.cnab_return_log_id.bank_account_id.acc_number} - REF: {self.your_number}",
            "ref": self.your_number,
            "is_cnab": True,
            "journal_id": self.journal_id.id,
            "currency_id": self.journal_id.currency_id.id
            or self.cnab_return_log_id.company_id.currency_id.id,
        }

    def create_account_move(self):
        move_obj = self.env["account.move"]
        move_vals = self._get_move_vals()
        move = move_obj.create(move_vals)
