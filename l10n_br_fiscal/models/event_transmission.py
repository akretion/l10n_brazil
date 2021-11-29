# Copyright (C) 2021 - TODAY Renato Lima - Akretion
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class EventTransmission(models.Model):
    _name = "l10n_br_fiscal.event.transmission"
    _description = "Generic Fiscal Document Event Transmission"

    event_id = fields.Many2one(
        comodel_name="l10n_br_fiscal.event",
        string="Event",
    )

    document_type_id = fields.Many2one(
        comodel_name="l10n_br_fiscal.document.type",
        string="Document Event",
    )

    document_service_id = fields.Many2one(
        comodel_name="l10n_br_fiscal.document.service",
        string="Document Event",
    )

    create_date = fields.Datetime(
        string="Create Date",
        readonly=True,
        index=True,
        default=fields.Datetime.now,
    )

    message_request_id = fields.Many2one(
        comodel_name="l10n_br_fiscal.document.service.message",
        string="Message Request",
        domain="[('document_service_id', '=', document_service_id)]",
    )

    service_request = fields.Text(string="Service Request")

    # TODO remove this fields
    file_request_id = fields.Many2one(
        comodel_name="ir.attachment",
        string="Request XML File",
        copy=False,
        readonly=True,
    )

    message_response_id = fields.Many2one(
        comodel_name="l10n_br_fiscal.document.service.message",
        string="Message Response",
        domain="[('document_service_id', '=', document_service_id)]",
    )

    service_response = fields.Text(string="Service Request")

    # TODO remove this fields
    file_response_id = fields.Many2one(
        comodel_name="ir.attachment",
        string="Response XML File",
        copy=False,
        readonly=True,
    )

    state = fields.Selection(
        selection=[
            ('todo', 'To Do'),
            ('done', 'Done')
        ],
        string="State",
    )
