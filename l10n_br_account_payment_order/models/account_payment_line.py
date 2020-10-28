# Copyright (C) 2016-Today - KMEE (<http://kmee.com.br>).
#  Luis Felipe Miléo - mileo@kmee.com.br
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.addons import decimal_precision as dp
from odoo.tools.float_utils import float_round as round

from ..constants import (
    AVISO_FAVORECIDO,
    CODIGO_FINALIDADE_TED,
    COMPLEMENTO_TIPO_SERVICO,
)


class AccountPaymentLine(models.Model):
    _inherit = 'account.payment.line'

    digitable_line = fields.Char(
        string='Linha Digitável',
    )

    percent_interest = fields.Float(
        string='Percentual de Juros',
        digits=dp.get_precision('Account'),
    )

    amount_interest = fields.Float(
        string='Valor Juros',
        compute='_compute_interest',
        digits=dp.get_precision('Account'),
    )

    own_number = fields.Char(
        string='Nosso Numero',
    )

    document_number = fields.Char(
        string='Número documento',
    )

    company_title_identification = fields.Char(
        string='Identificação Titulo Empresa',
    )

    doc_finality_code = fields.Selection(
        selection=COMPLEMENTO_TIPO_SERVICO,
        string='Complemento do Tipo de Serviço',
        help='Campo P005 do CNAB',
    )

    ted_finality_code = fields.Selection(
        selection=CODIGO_FINALIDADE_TED,
        string='Código Finalidade da TED',
        help='Campo P011 do CNAB',
    )

    complementary_finality_code = fields.Char(
        string='Código de finalidade complementar',
        size=2,
        help='Campo P013 do CNAB',
    )

    favored_warning = fields.Selection(
        selection=AVISO_FAVORECIDO,
        string='Aviso ao Favorecido',
        help='Campo P006 do CNAB',
        default='0',
    )

    rebate_value = fields.Float(
        string='Valor do Abatimento',
        help='Campo G045 do CNAB',
        default=0.00,
        digits=(13, 2),
    )

    discount_value = fields.Float(
        string='Valor do Desconto',
        digits=(13, 2),
        default=0.00,
        help='Campo G046 do CNAB',
    )

    interest_value = fields.Float(
        string='Valor da Mora',
        digits=(13, 2),
        default=0.00,
        help='Campo G047 do CNAB',
    )

    fee_value = fields.Float(
        string='Valor da Multa',
        digits=(13, 2),
        default=0.00,
        help='Campo G048 do CNAB',
    )

    # TODO - Mover seleção para o arquivo de Constantes,
    #  aguardando retorno para saber se existe diferença
    #  entre os Bancos, o CNAB 400 da Unicred e o 240 da
    #  Febraban v10.06 estão iguais, a seleção no arquivo
    #  de constantes está diferente.
    #  Caso exista diferença vai ser preciso fazer o mesmo
    #  que foi feito nos Codigos de Retorno
    movement_instruction_code = fields.Selection(
        string='Código da Instrução para Movimento',
        help='Campo G061 do CNAB',
        selection=[
            ('01', '01 - Remessa*'),
            ('02', '02 - Pedido de Baixa'),
            ('04', '04 - Concessão de Abatimento*'),
            ('05', '05 - Cancelamento de Abatimento'),
            ('06', '06 - Alteração de vencimento'),
            ('08', '08 - Alteração de Seu Número'),
            ('09', '09 - Protestar*'),
            ('11', '11 - Sustar Protesto e Manter em Carteira'),
            ('25', '25 - Sustar Protesto e Baixar Título'),
            ('26', '26 – Protesto automático'),
            ('31', '31 - Alteração de outros dados (Alteração de dados do pagador'),
            ('40', '40 - Alteração de Carteira')]
    )

    @api.multi
    @api.depends('percent_interest', 'amount_currency')
    def _compute_interest(self):
        for record in self:
            precision = record.env[
                'decimal.precision'].precision_get('Account')
            record.amount_interest = round(
                record.amount_currency * (
                    record.percent_interest / 100), precision)

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        mode = (
            self.env['account.payment.order']
            .browse(self.env.context.get('order_id'))
            .payment_mode_id
        )
        if mode.doc_finality_code:
            res.update({'doc_finality_code': mode.doc_finality_code})
        if mode.ted_finality_code:
            res.update({'ted_finality_code': mode.ted_finality_code})
        if mode.complementary_finality_code:
            res.update(
                {'complementary_finality_code': mode.complementary_finality_code}
            )
        if mode.favored_warning:
            res.update({'favored_warning': mode.favored_warning})

        return res
