# -*- coding: utf-8 -*-
# @ 2018 Akretion - www.akretion.com.br -
#   Magno Costa <magno.costa@akretion.com.br>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from openerp import models, fields


class PaymentMode(models.Model):
    _inherit = 'payment.mode'

    type_nf_payment = fields.Selection([
        ('01', u'01 - Dinheiro'),
        ('02', u'02 - Cheque'),
        ('03', u'03 - Cartão de Crédito'),
        ('04', u'04 - Cartão de Débito'),
        ('05', u'05 - Crédito Loja'),
        ('10', u'10 - Vale Alimentação'),
        ('11', u'11 - Vale Refeição'),
        ('12', u'12 - Vale Presente'),
        ('13', u'13 - Vale Combustível'),
        ('15', u'15 - Boleto Bancário'),
        ('90', u'90 - Sem pagamento'),
        ('99', u'99 - Outros')
    ], string='Tipo de Pagamento da NF', required=True,
        help=u'Obrigatório o preenchimento do Grupo Informações de Pagamento'
             u' para NF-e e NFC-e. Para as notas com finalidade de Ajuste'
             u' ou Devolução o campo Forma de Pagamento deve ser preenchido'
             u' com 90 - Sem Pagamento.'
    )
