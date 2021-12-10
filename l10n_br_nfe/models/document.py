# Copyright 2019 Akretion (Raphaël Valyi <raphael.valyi@akretion.com>)
# Copyright 2019 KMEE INFORMATICA LTDA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import re

from unicodedata import normalize

from odoo import api, fields, models

from odoo.addons.spec_driven_model.models import spec_models

from odoo.addons.l10n_br_fiscal.constants.fiscal import (
    DOCUMENT_ISSUER_COMPANY,
    MODELO_FISCAL_NFCE,
    MODELO_FISCAL_NFE,
)

from ..constants.nfe import (
    NFCE_DANFE_LAYOUTS,
    NFE_DANFE_LAYOUTS,
    NFE_ENVIRONMENTS,
    NFE_TRANSMISSIONS,
    NFE_VERSIONS,
)


class NFe(models.Model):
    _name = "l10n_br_fiscal.document"
    _inherit = [
        "l10n_br_fiscal.document",
        # "l10n_br_nfe.document.workflow",
        # "l10n_br_nfe.document.electronic",
    ]


class NFeSpec(spec_models.StackedModel):
    _name = "l10n_br_fiscal.document"
    _inherit = ["l10n_br_fiscal.document", "nfe.40.infnfe"]
    _stacked = "nfe.40.infnfe"
    _stack_skip = "nfe40_veicTransp"
    _field_prefix = "nfe40_"
    _schema_name = "nfe"
    _schema_version = "4.0.0"
    _odoo_module = "l10n_br_nfe"
    _spec_module = "odoo.addons.l10n_br_nfe_spec.models.v4_00.leiauteNFe"
    _spec_tab_name = "NFe"
    _nfe_search_keys = ["nfe40_Id"]

    # all m2o at this level will be stacked even if not required:
    _force_stack_paths = ("infnfe.total", "infnfe.infAdic", "infnfe.exporta")

    ##########################
    # NF-e spec related fields
    ##########################

    ##########################
    # NF-e tag: infNFe
    ##########################

    nfe40_versao = fields.Char(related="document_version")

    nfe_version = fields.Selection(
        selection=NFE_VERSIONS,
        string="NFe Version",
        copy=False,
        default=lambda self: self.env.user.company_id.nfe_version,
    )

    nfe40_Id = fields.Char(
        compute="_compute_nfe_data",
        inverse="_inverse_nfe40_Id",
    )

    def _inverse_nfe40_Id(self):
        for record in self:
            if record.nfe40_Id:
                record.document_key = re.findall(r"\d+", str(record.nfe40_Id))[0]

    ##########################
    # NF-e tag: ide
    ##########################

    nfe40_cUF = fields.Char( # TODO criar uma função para tratar quando for entrada
        related="company_id.partner_id.state_id.ibge_code",
        string="nfe40_cUF",
    )

    # <cNF>17983659</cNF> TODO

    nfe40_natOp = fields.Char(related="operation_name")

    nfe40_mod = fields.Char(related="document_type_id.code", string="nfe40_mod")

    nfe40_serie = fields.Char(related="document_serie")

    nfe40_nNF = fields.Char(related="document_number")

    nfe40_dhEmi = fields.Datetime(related="document_date")

    nfe40_dhSaiEnt = fields.Datetime(related="date_in_out")

    nfe40_tpNF = fields.Selection(
        compute="_compute_nfe_data",
        inverse="_inverse_nfe40_tpNF",
    )

    nfe40_idDest = fields.Selection(compute="_compute_nfe40_idDest")

    cMunFG = fields.Char(related="company_id.partner_id.city_id.ibge_code")

    danfe_layout = fields.Selection(
        selection=NFE_DANFE_LAYOUTS + NFCE_DANFE_LAYOUTS,
        string="Danfe Layout",
    )

    nfe40_tpImp = fields.Selection(
        compute="_compute_nfe_data",
        inverse="_inverse_nfe40_tpImp",
    )

    nfe_transmission = fields.Selection(
        selection=NFE_TRANSMISSIONS,
        string="NFe Transmission",
        copy=False,
        default=lambda self: self.env.user.company_id.nfe_transmission,
    )

    nfe40_tpEmis = fields.Selection(
        compute="_compute_nfe_data",
        inverse="_inverse_nfe40_tpEmis",
    )

    # <cDV>0</cDV> TODO

    nfe_environment = fields.Selection(
        selection=NFE_ENVIRONMENTS,
        string="NFe Environment",
        copy=False,
        default=lambda self: self.env.user.company_id.nfe_environment,
    )

    nfe40_tpAmb = fields.Selection(related="nfe_environment")

    nfe40_finNFe = fields.Selection(related="edoc_purpose")

    nfe40_indFinal = fields.Selection(related="ind_final")

    nfe40_indPres = fields.Selection(related="ind_pres")

    nfe40_procEmi = fields.Selection(default="0")

    nfe40_verProc = fields.Char(
        copy=False,
        default=lambda s: s.env["ir.config_parameter"]
        .sudo()
        .get_param("l10n_br_nfe.version.name", default="Odoo Brasil OCA v12.0"),
    )

    @api.depends("fiscal_operation_type", "nfe_transmission")
    def _compute_nfe_data(self):
        """Set schema data which are not just related fields"""
        for record in self:
            # id
            if record.document_type_id and record.document_type_id.prefix:
                record.nfe40_Id = record.document_type_id.prefix + record.document_key
            else:
                record.nfe40_Id = None

            # tpNF
            if record.fiscal_operation_type:
                operation_2_tpNF = {
                    "out": "1",
                    "in": "0",
                }
                record.nfe40_tpNF = operation_2_tpNF[record.fiscal_operation_type]

            # TpEmis
            if record.nfe_transmission:
                record.nfe40_tpEmis = record.nfe_transmission

            # tpImp
            if record.issuer == DOCUMENT_ISSUER_COMPANY:
                if record.document_type_id.code == MODELO_FISCAL_NFE:
                    record.nfe40_tpImp = record.company_id.nfe_danfe_layout

                if record.document_type_id.code == MODELO_FISCAL_NFCE:
                    record.nfe40_tpImp = record.company_id.nfce_danfe_layout

    def _inverse_nfe40_tpNF(self):
        for rec in self:
            if rec.nfe40_tpNF:
                tpNF_2_operation = {
                    "1": "out",
                    "0": "in",
                }
                rec.fiscal_operation_type = tpNF_2_operation[rec.nfe40_tpNF]

    def _inverse_nfe40_tpEmis(self):
        for record in self:
            if record.nfe40_tpEmis:
                record.nfe_transmission = record.nfe40_tpEmis

    def _inverse_nfe40_tpImp(self):
        for record in self:
            if record.nfe40_tpImp:
                record.danfe_layout = record.nfe40_tpImp

    ##########################
    # NF-e tag: NFref
    ##########################

    nfe40_NFref = fields.One2many(
        comodel_name="l10n_br_fiscal.document.related",
        related="document_related_ids",
        inverse_name="document_id",
    )

    ##########################
    # NF-e tag: emit
    ##########################

    # emit and dest are not related fields as their related fields
    # can change depending if it's and incoming our outgoing NFe
    # specially when importing (ERP NFe migration vs supplier Nfe).
    nfe40_emit = fields.Many2one(
        comodel_name="res.company",
        compute="_compute_emit",
        readonly=True,
        string="Emit",
    )

    nfe40_CRT = fields.Selection(
        related="company_tax_framework",
        string="Código de Regime Tributário (NFe)",
    )

    def _compute_emit(self):
        for doc in self:  # TODO if out
            doc.nfe40_emit = doc.company_id

    ##########################
    # NF-e tag: dest
    ##########################

    nfe40_dest = fields.Many2one(
        comodel_name="res.partner",
        compute="_compute_dest",
        readonly=True,
        string="Dest",
    )

    nfe40_indIEDest = fields.Selection(
        related="partner_ind_ie_dest",
        string="Contribuinte do ICMS (NFe)",
    )

    @api.depends("partner_id")
    def _compute_dest(self):
        for doc in self:  # TODO if out
            doc.nfe40_dest = doc.partner_id

    @api.depends("partner_id", "company_id")
    def _compute_nfe40_idDest(self):
        for rec in self:
            if rec.company_id.partner_id.state_id == rec.partner_id.state_id:
                rec.nfe40_idDest = "1"
            elif rec.company_id.partner_id.country_id == rec.partner_id.country_id:
                rec.nfe40_idDest = "2"
            else:
                rec.nfe40_idDest = "3"

    ##########################
    # NF-e tag: det
    ##########################

    # TODO should be done by framework?
    nfe40_det = fields.One2many(
        comodel_name="l10n_br_fiscal.document.line",
        inverse_name="document_id",
        related="line_ids",
    )

    ##########################
    # NF-e tag: ICMSTot
    ##########################

    nfe40_vBC = fields.Monetary(string="BC do ICMS", related="amount_icms_base")

    nfe40_vICMS = fields.Monetary(related="amount_icms_value")

    # <vICMSDeson>0.00</vICMSDeson>

    nfe40_vFCPUFDest = fields.Monetary(related="amount_icmsfcp_value")

    nfe40_vICMSUFDest = fields.Monetary(related="amount_icms_destination_value")

    nfe40_vICMSUFRemet = fields.Monetary(related="amount_icms_origin_value")

    # <vFCP>0.00</vFCP> TODO

    nfe40_vBCST = fields.Monetary(related="amount_icmsst_base")

    nfe40_vST = fields.Monetary(related="amount_icmsst_value")

    # <vFCPST>0.00</vFCPST> TODO

    # <vFCPSTRet>0.00</vFCPSTRet> TODO

    nfe40_vProd = fields.Monetary(related="amount_price_gross")

    nfe40_vFrete = fields.Monetary(related="amount_freight_value")

    nfe40_vSeg = fields.Monetary(related="amount_insurance_value")

    nfe40_vDesc = fields.Monetary(related="amount_discount_value")

    nfe40_vII = fields.Monetary(related="amount_ii_value")

    nfe40_vIPI = fields.Monetary(related="amount_ipi_value")

    # <vIPIDevol>0.00</vIPIDevol> TODO

    nfe40_vPIS = fields.Monetary(
        string="Valor do PIS (NFe)", related="amount_pis_value"
    )

    nfe40_vCOFINS = fields.Monetary(
        string="valor do COFINS (NFe)", related="amount_cofins_value"
    )

    nfe40_vOutro = fields.Monetary(related="amount_other_value")

    nfe40_vNF = fields.Monetary(related="amount_total")

    nfe40_vTotTrib = fields.Monetary(related="amount_estimate_tax")

    ##########################
    # NF-e tag: transp
    ##########################

    nfe40_modFrete = fields.Selection(default="9")

    ##########################
    # NF-e tag: transporta
    ##########################

    nfe40_transporta = fields.Many2one(comodel_name="res.partner")

    ##########################
    # NF-e tag: pag
    ##########################

    def _prepare_amount_financial(self, ind_pag, t_pag, v_pag):
        return {
            "nfe40_indPag": ind_pag,
            "nfe40_tPag": t_pag,
            "nfe40_vPag": v_pag,
        }

    def _export_fields_pagamentos(self):
        if not self.amount_financial_total:
            self.nfe40_detPag = [
                (5, 0, 0),
                (0, 0, self._prepare_amount_financial("0", "90", 0.00)),
            ]
        self.nfe40_detPag.__class__._field_prefix = "nfe40_"

    ##########################
    # NF-e tag: infAdic
    ##########################

    nfe40_infAdFisco = fields.Char(compute="_compute_nfe40_additional_data")

    ##########################
    # NF-e tag: infCpl
    ##########################

    nfe40_infCpl = fields.Char(compute="_compute_nfe40_additional_data")

    @api.depends("fiscal_additional_data", "fiscal_additional_data")
    def _compute_nfe40_additional_data(self):
        for record in self:
            record.nfe40_infCpl = False
            record.nfe40_infAdFisco = False
            if record.fiscal_additional_data:
                record.nfe40_infAdFisco = (
                    normalize("NFKD", record.fiscal_additional_data)
                    .encode("ASCII", "ignore")
                    .decode("ASCII")
                    .replace("\n", "")
                    .replace("\r", "")
                )
            if record.customer_additional_data:
                record.nfe40_infCpl = (
                    normalize("NFKD", record.customer_additional_data)
                    .encode("ASCII", "ignore")
                    .decode("ASCII")
                    .replace("\n", "")
                    .replace("\r", "")
                )

    ##########################
    # NF-e tag: infRespTec
    ##########################

    nfe40_infRespTec = fields.Many2one(
        comodel_name="res.partner",
        related="company_id.technical_support_id",
    )

    ################################
    # Framework Spec model's methods
    ################################

    def _export_field(self, xsd_field, class_obj, member_spec):
        if xsd_field == "nfe40_tpAmb":
            self.env.context = dict(self.env.context)
            self.env.context.update({"tpAmb": self[xsd_field]})
        elif xsd_field == "nfe40_fat" and (
            self.nfe40_detPag and self.nfe40_detPag[0].nfe40_tPag != "90"
        ):
            self._stacking_points["nfe40_fat"] = self._fields["nfe40_fat"]
            res = super()._export_field(xsd_field, class_obj, member_spec)
            self._stacking_points.pop("nfe40_fat")
            return res
        elif xsd_field == "nfe40_vTroco" and (
            self.nfe40_detPag and self.nfe40_detPag[0].nfe40_tPag == "90"
        ):
            return False
        return super()._export_field(xsd_field, class_obj, member_spec)

    def _export_many2one(self, field_name, xsd_required, class_obj=None):
        self.ensure_one()
        if field_name in self._stacking_points.keys():
            if field_name == "nfe40_ISSQNtot" and not any(
                t == "issqn"
                for t in self.nfe40_det.mapped("product_id.tax_icms_or_issqn")
            ):
                return False

            elif (not xsd_required) and field_name not in ["nfe40_enderDest"]:
                comodel = self.env[self._stacking_points.get(field_name).comodel_name]
                fields = [
                    f for f in comodel._fields if f.startswith(self._field_prefix)
                ]
                sub_tag_read = self.read(fields)[0]
                if not any(
                    v
                    for k, v in sub_tag_read.items()
                    if k.startswith(self._field_prefix)
                ):
                    return False

        return super()._export_many2one(field_name, xsd_required, class_obj)

    def _export_one2many(self, field_name, class_obj=None):
        res = super()._export_one2many(field_name, class_obj)
        i = 0
        for field_data in res:
            i += 1
            if class_obj._fields[field_name].comodel_name == "nfe.40.det":
                field_data.nItem = i
        return res

    def _build_attr(self, node, fields, vals, path, attr):
        key = "nfe40_%s" % (attr.get_name(),)  # TODO schema wise
        value = getattr(node, attr.get_name())

        if key == "nfe40_mod":
            vals["document_type_id"] = (
                self.env["l10n_br_fiscal.document.type"]
                .search([("code", "=", value)], limit=1)
                .id
            )

        return super()._build_attr(node, fields, vals, path, attr)

    def _build_many2one(self, comodel, vals, new_value, key, value, path):
        if key == "nfe40_emit" and self.env.context.get("edoc_type") == "in":
            enderEmit_value = self.env["res.partner"].build_attrs(
                value.enderEmit, path=path
            )
            new_value.update(enderEmit_value)
            new_value["is_company"] = True
            new_value["cnpj_cpf"] = new_value.get("nfe40_CNPJ")
            super()._build_many2one(
                self.env["res.partner"], vals, new_value, "partner_id", value, path
            )
        elif self.env.context.get("edoc_type") == "in" and key in [
            "nfe40_dest",
            "nfe40_enderDest",
        ]:
            # this would be the emit/company data, but we won't update it on
            # NFe import so just do nothing
            return
        elif (
            self._name == "account.invoice"
            and comodel._name == "l10n_br_fiscal.document"
        ):
            # module l10n_br_account_nfe
            # stacked m2o
            vals.update(new_value)
        else:
            super()._build_many2one(comodel, vals, new_value, key, value, path)
