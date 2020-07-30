# Copyright 2019 KMEE INFORMATICA LTDA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from requests import Session
import logging

from erpbrasil.assinatura import certificado as cert
from erpbrasil.transmissao import TransmissaoSOAP
from erpbrasil.base import misc
from erpbrasil.edoc.nfse import NFSeFactory

from odoo import api, fields, models, _
from odoo.addons.l10n_br_fiscal.constants.fiscal import (
    MODELO_FISCAL_NFSE,
    SITUACAO_EDOC_AUTORIZADA,
    TAX_FRAMEWORK_SIMPLES_ALL,
)
from ..constants.nfse import (
    NFSE_ENVIRONMENTS,
    OPERATION_NATURE,
    RPS_TYPE,
    TAXATION_SPECIAL_REGIME,
)

from .res_company import PROCESSADOR

_logger = logging.getLogger(__name__)


def fiter_processador_edoc_nfse(record):
    if (record.processador_edoc == PROCESSADOR and
            record.document_type_id.code in [
                MODELO_FISCAL_NFSE,
            ]):
        return True
    return False


def fiter_provedor_ginfes(record):
    if record.company_id.provedor_nfse == 'ginfes':
        return True
    return False


class Document(models.Model):

    _inherit = 'l10n_br_fiscal.document'

    edoc_error_message = fields.Text(
        readonly=True,
        copy=False,
    )

    rps_number = fields.Char(
        string='RPS Number',
        copy=False,
        index=True,
    )
    rps_type = fields.Selection(
        string='RPS Type',
        selection=RPS_TYPE,
        default='1',
    )
    operation_nature = fields.Selection(
        string='Operation Nature',
        selection=OPERATION_NATURE,
        default='1',
    )
    taxation_special_regime = fields.Selection(
        string='Taxation Special Regime',
        selection=TAXATION_SPECIAL_REGIME,
        default='1',
    )
    verify_code = fields.Char(
        string='Verify Code',
        readonly=True,
    )
    nfse_environment = fields.Selection(
        selection=NFSE_ENVIRONMENTS,
        string="NFSe Environment",
        default=lambda self: self.env.user.company_id.nfse_environment,
    )

    @api.model
    def create(self, values):
        if not values.get('date'):
            values['date'] = self._date_server_format()

        if values.get('company_id'):
            company_obj = self.env['res.company']
            company = company_obj.browse(values['company_id'])
            if company.provedor_nfse == 'ginfes':
                if values.get('document_serie_id') and \
                        not values.get('rps_number'):
                    serie_id = self.document_serie_id.browse(
                        values['document_serie_id'])
                    values['rps_number'] = serie_id.next_seq_number()
                values['number'] = None
        return super(Document, self).create(values)

    def _generate_key(self):
        remaining = self - self.filtered(fiter_processador_edoc_nfse)
        if remaining:
            super(Document, remaining)._generate_key()

    def _processador_erpbrasil_nfse(self):
        certificado = cert.Certificado(
            arquivo=self.company_id.certificate_nfe_id.file,
            senha=self.company_id.certificate_nfe_id.password
        )
        session = Session()
        session.verify = False
        transmissao = TransmissaoSOAP(certificado, session)
        return NFSeFactory(
            transmissao=transmissao,
            ambiente=self.nfse_environment,
            cidade_ibge=int('%s%s' % (
                self.company_id.partner_id.state_id.ibge_code,
                self.company_id.partner_id.city_id.ibge_code
            )),
            cnpj_prestador=misc.punctuation_rm(
                self.company_id.partner_id.cnpj_cpf),
            im_prestador=misc.punctuation_rm(
                self.company_id.partner_id.inscr_mun or ''),
        )

    @api.multi
    def _document_export(self, pretty_print=True):
        super(Document, self)._document_export()
        for record in self.filtered(fiter_processador_edoc_nfse):
            edoc = record.serialize()[0]
            processador = record._processador_erpbrasil_nfse()
            xml_file = processador.\
                _generateds_to_string_etree(edoc, pretty_print=pretty_print)[0]
            event_id = self._gerar_evento(xml_file, event_type="0")
            _logger.debug(xml_file)
            record.autorizacao_event_id = event_id

    def _prepare_dados_servico(self):
        self.line_ids.ensure_one()
        result = {
            'codigo_cnae': None,
        }
        result.update(self.line_ids.prepare_line_servico())
        result.update(self.company_id.prepare_company_servico())

        return result

    def _prepare_dados_tomador(self):
        result = self.partner_id.prepare_partner_tomador(
            self.company_id.country_id.id)

        result.update(
            {'complemento': self.partner_shipping_id.street2 or None})

        return result

    def _prepare_lote_rps(self):
        num_rps = self.rps_number

        dh_emi = fields.Datetime.context_timestamp(
            self, fields.Datetime.from_string(self.date)
        ).strftime('%Y-%m-%dT%H:%M:%S')
        return {
            'cnpj': misc.punctuation_rm(self.company_id.partner_id.cnpj_cpf),
            'inscricao_municipal': misc.punctuation_rm(
                self.company_id.partner_id.inscr_mun or '') or None,
            'id': 'rps' + str(num_rps),
            'numero': num_rps,
            'serie': self.document_serie_id.code or '',
            'tipo': self.rps_type,
            'data_emissao': dh_emi,
            'natureza_operacao': self.operation_nature,
            'regime_especial_tributacao': self.taxation_special_regime,
            'optante_simples_nacional': '1'
            if self.company_id.tax_framework in TAX_FRAMEWORK_SIMPLES_ALL
            else '2',
            'incentivador_cultural': '1'
            if self.company_id.cultural_encourager else '2',
            'status': '1',
            'rps_substitiuido': None,
            'intermediario_servico': None,
            'construcao_civil': None,
        }

    @api.multi
    def _eletronic_document_send(self):
        super(Document, self)._eletronic_document_send()
        for record in self.filtered(fiter_processador_edoc_nfse):
            processador = record._processador_erpbrasil_nfse()

            protocolo = record.protocolo_autorizacao
            vals = dict()

            if not protocolo:
                for edoc in record.serialize():
                    processo = None
                    for p in processador.processar_documento(edoc):
                        processo = p

                        if processo.webservice == 'RecepcionarLoteRpsV3':
                            if processo.resposta.Protocolo is None:
                                mensagem_completa = ''
                                if processo.resposta.ListaMensagemRetorno:
                                    lista_msgs = processo.resposta.ListaMensagemRetorno
                                    for mr in lista_msgs.MensagemRetorno:

                                        correcao = ''
                                        if mr.Correcao:
                                            correcao = mr.Correcao

                                        mensagem_completa += (
                                            mr.Codigo + ' - ' +
                                            mr.Mensagem +
                                            ' - Correção: ' +
                                            correcao + '\n'
                                        )
                                vals['edoc_error_message'] = mensagem_completa
                                record.write(vals)
                                return
                            protocolo = processo.resposta.Protocolo

                    if processo.webservice == 'ConsultarSituacaoLoteRpsV3':
                        vals['codigo_situacao'] = processo.resposta.Situacao
            else:
                vals['codigo_situacao'] = 4

            if vals.get('codigo_situacao') == 1:
                vals['motivo_situacao'] = _('Não Recebido')

            elif vals.get('codigo_situacao') == 2:
                vals['motivo_situacao'] = _('Lote ainda não processado')

            elif vals.get('codigo_situacao') == 3:
                vals['motivo_situacao'] = _('Procesado com Erro')

            elif vals.get('codigo_situacao') == 4:
                vals['motivo_situacao'] = _('Procesado com Sucesso')
                vals['protocolo_autorizacao'] = protocolo

            if vals.get('codigo_situacao') in (3, 4):
                processo = processador.consultar_lote_rps(protocolo)

                if processo.resposta:
                    mensagem_completa = ''
                    if processo.resposta.ListaMensagemRetorno:
                        lista_msgs = processo.resposta.ListaMensagemRetorno
                        for mr in lista_msgs.MensagemRetorno:

                            correcao = ''
                            if mr.Correcao:
                                correcao = mr.Correcao

                            mensagem_completa += (
                                mr.Codigo + ' - ' +
                                mr.Mensagem +
                                ' - Correção: ' +
                                correcao + '\n'
                            )
                    vals['edoc_error_message'] = mensagem_completa

                if processo.resposta.ListaNfse:
                    xml_file = processador._generateds_to_string_etree(
                        processo.resposta)[0]
                    record.autorizacao_event_id.set_done(xml_file)
                    for comp in processo.resposta.ListaNfse.CompNfse:
                        vals['number'] = comp.Nfse.InfNfse.Numero
                        vals['data_hora_autorizacao'] = \
                            comp.Nfse.InfNfse.DataEmissao
                        vals['verify_code'] = \
                            comp.Nfse.InfNfse.CodigoVerificacao
                    record._change_state(SITUACAO_EDOC_AUTORIZADA)

            record.write(vals)
        return
