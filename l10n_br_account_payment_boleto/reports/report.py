# -*- coding: utf-8 -*-
#    Copyright (C) 2012-TODAY KMEE (http://www.kmee.com.br)
#    @author Luis Felipe Miléo (mileo@kmee.com.br)
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from __future__ import with_statement

from openerp import pooler
from openerp.exceptions import Warning as UserError
from openerp.report.interface import report_int
from openerp.report.render import render
from openerp import _

from ..boleto.document import Boleto


class ExternalPdf(render):

    def __init__(self, pdf):
        render.__init__(self)
        self.pdf = pdf
        self.output_type = 'pdf'

    def _render(self):
        return self.pdf


class ReportCustom(report_int):
    """
        Custom report for return boletos
    """

    def create(self, cr, uid, ids, datas, context=False):
        if not context:
            context = {}
        active_ids = context.get('active_ids')
        active_model = context.get('active_model')
        pool = pooler.get_pool(cr.dbname)
        ids_move_lines = []

        aml_obj = pool.get('account.move.line')

        if active_model == 'account.invoice':
            ai_obj = pool.get('account.invoice')
            for account_invoice in ai_obj.browse(cr, uid, active_ids):
                for move_line in account_invoice.move_line_receivable_id:
                    ids_move_lines.append(move_line.id)
        elif active_model == 'account.move.line':
            ids_move_lines = active_ids
        else:
            return False

        boleto_list = aml_obj.send_payment(cr, uid, ids_move_lines)
        if not boleto_list:
            raise UserError(_('Não é possível gerar os boletos\n'
                            'Certifique-se que a fatura esteja confirmada e o '
                            'forma de pagamento seja duplicatas'))
        pdf_string = Boleto.get_pdfs(boleto_list)
        self.obj = ExternalPdf(pdf_string)
        self.obj.render()
        return self.obj.pdf, 'pdf'


ReportCustom('report.l10n_br_account_payment_boleto.report')
