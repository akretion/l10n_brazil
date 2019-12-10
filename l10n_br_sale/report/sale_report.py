# Copyright (C) 2011  Renato Lima - Akretion
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import models, fields


class SaleReport(models.Model):
    _inherit = "sale.report"

    fiscal_operation_id = fields.Many2one(
        'l10n_br_fiscal.operation',
        'Fiscal Operation',
        readonly=True)

    def _select(self):
        return super(SaleReport, self)._select() + \
            ", l.fiscal_operation_id as fiscal_operation_id, " \

    def _group_by(self):
        return super(SaleReport, self)._group_by() + \
            ", l.fiscal_operation_id, l.fiscal_operation_id"
