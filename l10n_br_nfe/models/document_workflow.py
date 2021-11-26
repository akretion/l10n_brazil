# Copyright (C) 2019  Renato Lima - Akretion
# Copyright (C) 2019  KMEE INFORMATICA LTDA
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from erpbrasil.base.fiscal.edoc import ChaveEdoc

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class NFeWorkflow(models.AbstractModel):
    _name = "l10n_br_nfe.document.workflow"
    _description = "NFe Document Workflow"
    _inherit = "l10n_br_fiscal.document.workflow"

    def _document_number(self):
        # TODO: Criar campos no fiscal para codigo aleatorio e digito verificador,
        # pois outros modelos também precisam desses campos: CT-e, MDF-e etc
        super()._document_number()
        for record in self.filtered(filter_processador_edoc_nfe):
            if record.document_key:
                try:
                    chave = ChaveEdoc(record.document_key)
                    record.nfe40_cNF = chave.codigo_aleatorio
                    record.nfe40_cDV = chave.digito_verificador
                except Exception as e:
                    raise ValidationError(
                        _("{}:\n {}".format(record.document_type_id.name, e))
                    )

    def _document_date(self):
        super()._document_date()
        for record in self.filtered(filter_processador_edoc_nfe):
            if not record.date_in_out:
                record.date_in_out = fields.Datetime.now()
