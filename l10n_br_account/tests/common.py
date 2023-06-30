import base64
import json
import time
from unittest import SkipTest

import mock
from unittest.mock import patch
from lxml import etree

from odoo import fields
from odoo.exceptions import UserError
from odoo.models import NewId
from odoo.tests import SavepointCase
from odoo.tests.common import Form, TransactionCase, tagged

from odoo.addons.account.tests.common import AccountTestInvoicingCommon

from odoo.addons.l10n_br_fiscal.constants.fiscal import (
    CFOP_DESTINATION_EXTERNAL,
    CFOP_DESTINATION_INTERNAL,
    TAX_DOMAIN_ICMS,
    TAX_DOMAIN_ISSQN,
    TAX_FRAMEWORK_NORMAL,
    TAX_FRAMEWORK_SIMPLES,
    TAX_FRAMEWORK_SIMPLES_ALL,
)


@tagged("post_install", "-at_install")
class Common(AccountTestInvoicingCommon):
    """
    This is the base test suite for l10n_br_account with proper Brazilian
    Charts of Accounts and Brazilian data.
    """

    @classmethod
    def setUpClass(cls, chart_template_ref=None):
        super().setUpClass(chart_template_ref)
        cls.env.user.groups_id |= cls.env.ref("l10n_br_fiscal.group_manager")
#        cls.product_a = cls.env.ref("product.product_product_27")
#        cls.product_b = cls.env.ref("product.product_product_12")
        # TODO would be better to write in these created products properly:
        cls.product_a.write(
            {
                "ncm_id": cls.env.ref("l10n_br_fiscal.ncm_94033000").id,
                "fiscal_genre_id": cls.env.ref("l10n_br_fiscal.product_genre_94").id,
                "fiscal_type": "00",
                "icms_origin": "5",
                "taxes_id": False,
                "tax_icms_or_issqn": "icms",
                "uoe_id": cls.env.ref("uom.product_uom_kgm").id,
            }
        )
        cls.fiscal_type_product_product_a_sn = cls.env["ir.property"].create(
            {
                "name": "fiscal_type",
                "fields_id": cls.env["ir.model.fields"].search([("model", "=", "product.template"), ("name", "=", "fiscal_type")]).id,
                "value": "04",
                "type": "selection",
                "res_id": cls.product_a.id,
            }
        )
        cls.fiscal_origin_product_product_a_sn = cls.env["ir.property"].create(
            {
                "name": "fiscal_origin",
                "fields_id": cls.env["ir.model.fields"].search([("model", "=", "product.template"), ("name", "=", "icms_origin")]).id,
                "value": "5",
                "type": "selection",
                "res_id": cls.product_a.id,
            }
        )

        cls.product_b.write(
            {
                'lst_price': 1000.0,
                "ncm_id": cls.env.ref("l10n_br_fiscal.ncm_94013090").id,
                "fiscal_genre_id": cls.env.ref("l10n_br_fiscal.product_genre_94").id,
                "fiscal_type": "00",
                "icms_origin": "0",
                "taxes_id": False,
                "tax_icms_or_issqn": "icms",
                "uoe_id": cls.env.ref("uom.product_uom_kgm").id,
            }
        )
        cls.fiscal_type_product_product_b_sn = cls.env["ir.property"].create(
            {
                "name": "fiscal_type",
                "fields_id": cls.env["ir.model.fields"].search([("model", "=", "product.template"), ("name", "=", "fiscal_type")]).id,
                "value": "00",
                "type": "selection",
                "res_id": cls.product_b.id,
            }
        )
        cls.fiscal_origin_product_product_b_sn = cls.env["ir.property"].create(
            {
                "name": "fiscal_origin",
                "fields_id": cls.env["ir.model.fields"].search([("model", "=", "product.template"), ("name", "=", "icms_origin")]).id,
                "value": "0",
                "type": "selection",
                "res_id": cls.product_b.id,
            }
        )

        cls.partner_a.write({
            "cnpj_cpf": "49.190.159/0001-05",
            "is_company": "1",
            "ind_ie_dest": "1",
            "tax_framework": "3",
            "legal_name": "partner A",
            "country_id": cls.env.ref("base.br").id,
            "district": "Centro",
            "zip": "01311-915",
            "fiscal_profile_id": cls.env.ref("l10n_br_fiscal.partner_fiscal_profile_snc").id,
        })
        cls.partner_b.write({
            "cnpj_cpf": "42.591.651/0001-43",
            "is_company": "0",
            "legal_name": "partner B",
            "country_id": cls.env.ref("base.br").id,
            "district": "Na PQP",
            "zip": "01311-942",
            "fiscal_profile_id": cls.env.ref("l10n_br_fiscal.partner_fiscal_profile_cnt").id,
        })

        cls.partner_c = cls.partner_a.copy({
            "name": "partner_c",
            "cnpj_cpf": "67.405.936/0001-73",
            "legal_name": "partner C",
            "fiscal_profile_id": cls.env.ref("l10n_br_fiscal.partner_fiscal_profile_ncn").id,
        })

    @classmethod
    def setup_company_data(cls, company_name, chart_template=None, **kwargs):
        if company_name == "company_2_data":
            company_name = "empresa 2 Simples Nacional"
            chart_template = cls.env.ref(
                "l10n_br_coa_simple.l10n_br_coa_simple_chart_template"
            )
        elif company_name == "company_1_data":
            company_name = "empresa 1 Lucro Presumido"
            chart_template = cls.env.ref(
                "l10n_br_coa_generic.l10n_br_coa_generic_template"
            )
        return super().setup_company_data(
            company_name,
            chart_template,
            country_id=cls.env.ref("base.br").id,
            currency_id=cls.env.ref("base.BRL").id,
            **kwargs
        )

    @classmethod
    def init_invoice(
        cls,
        move_type,
        partner=None,
        invoice_date=None,
        post=False,
        products=None,
        amounts=None,
        taxes=None,
        currency=None,
        document_type=None,
        document_serie=None,
        fiscal_operation=None,
        fiscal_operation_lines=None,
    ):
        """
        We could not override the super one because we need to inject extra fiscal fields.
        """
        products = [] if products is None else products
        amounts = [] if amounts is None else amounts
        move_form = Form(
            cls.env["account.move"].with_context(
                default_move_type=move_type,
                account_predictive_bills_disable_prediction=True,
            )
        )
        move_form.invoice_date = invoice_date or fields.Date.from_string("2019-01-01")
        move_form.date = move_form.invoice_date
        move_form.partner_id = partner or cls.partner_a
        move_form.currency_id = currency if currency else cls.company_data["currency"]

        # extra BR fiscal params:
        move_form.document_type_id = document_type
        move_form.document_serie_id = document_serie
        move_form.fiscal_operation_id = fiscal_operation

        for index, product in enumerate(products):
            with move_form.invoice_line_ids.new() as line_form:
                line_form.product_id = product

                line_form.fiscal_operation_line_id = fiscal_operation_lines[index]

                if taxes:
                    line_form.tax_ids.clear()
                    line_form.tax_ids.add(taxes)

        for amount in amounts:
            with move_form.invoice_line_ids.new() as line_form:
                line_form.name = "test line"
                # We use account_predictive_bills_disable_prediction context key so that
                # this doesn't trigger prediction in case enterprise (hence account_predictive_bills) is installed
                line_form.price_unit = amount
                if taxes:
                    line_form.tax_ids.clear()
                    for tax in taxes:
                        line_form.tax_ids.add(tax)

        rslt = move_form.save()

        if post:
            rslt.action_post()

        return rslt


@tagged("post_install", "-at_install")
class AccountMoveSN(Common):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.icms_tax_definition_empresa_simples_nacional = cls.env[
            "l10n_br_fiscal.tax.definition"
        ].create({
            "company_id": cls.company_data["company"].id,
            "tax_group_id": cls.env.ref("l10n_br_fiscal.tax_group_icmssn").id,
            "is_taxed": True,
            "is_debit_credit": True,
            "custom_tax": True,
            "tax_id": cls.env.ref("l10n_br_fiscal.tax_icms_sn_com_credito").id,
            "cst_id": cls.env.ref("l10n_br_fiscal.cst_icmssn_101").id,
            "state": "approved",
        })

        cls.empresa_sn_document_55_serie_1 = cls.env[
            "l10n_br_fiscal.document.serie"
        ].create(
            {
                "code": "1",
                "name": "Série 1",
                "document_type_id": cls.env.ref("l10n_br_fiscal.document_55").id,
                #                "company_id": cls.company_data["company"].id,
                "active": True,
            }
        )
        #        cls.invoice = cls.init_invoice('out_invoice', products=cls.product_a+cls.product_b)
        cls.invoice = cls.init_invoice(
            "out_invoice",
            products=cls.product_a + cls.product_b,  # FIXME
#            products=cls.product_a + cls.product_a,
            document_type=cls.env.ref("l10n_br_fiscal.document_55"),
            document_serie=cls.empresa_sn_document_55_serie_1,
            fiscal_operation=cls.env.ref("l10n_br_fiscal.fo_venda"),
            fiscal_operation_lines=[
                cls.env.ref("l10n_br_fiscal.fo_venda_revenda"),
                cls.env.ref("l10n_br_fiscal.fo_venda_revenda"),
            ],
        )

        cls.product_line_vals_1 = {
            "name": cls.product_a.name,
            "product_id": cls.product_a.id,
            "account_id": cls.product_a.property_account_income_id.id,
            "partner_id": cls.partner_a.id,
            "product_uom_id": cls.product_a.uom_id.id,
            "quantity": 1.0,
            "discount": 0.0,
            "price_unit": 1000.0,
            "price_subtotal": 1000.0,
            "price_total": 1000.0,
            "tax_line_id": False,
            "currency_id": cls.company_data["currency"].id,
            "amount_currency": -973.0,
            "debit": 0.0,
            "credit": 1000.0,
            "date_maturity": False,
            "tax_exigible": True,
        }

        cls.product_line_vals_2 = {
            "name": cls.product_b.name,
            "product_id": cls.product_b.id,
            "account_id": cls.product_b.property_account_income_id.id,
            "partner_id": cls.partner_a.id,
            "product_uom_id": cls.product_b.uom_id.id,
            "quantity": 1.0,
            "discount": 0.0,
            "price_unit": 200.0,
            "price_subtotal": 200.0,
            "price_total": 260.0,
            "tax_line_id": False,
            "currency_id": cls.company_data["currency"].id,
            "amount_currency": -200.0,
            "debit": 0.0,
            "credit": 200.0,
            "date_maturity": False,
            "tax_exigible": True,
        }

        cls.tax_line_vals_1 = {
            "name": cls.tax_sale_a.name,
            "product_id": False,
            "account_id": cls.company_data["default_account_tax_sale"].id,
            "partner_id": cls.partner_a.id,
            "product_uom_id": False,
            "quantity": 1.0,
            "discount": 0.0,
            "price_unit": 180.0,
            "price_subtotal": 180.0,
            "price_total": 180.0,
            "tax_ids": [],
            "tax_line_id": cls.tax_sale_a.id,
            "currency_id": cls.company_data["currency"].id,
            "amount_currency": -180.0,
            "debit": 0.0,
            "credit": 180.0,
            "date_maturity": False,
            "tax_exigible": True,
        }

        cls.tax_line_vals_2 = {
            "name": cls.tax_sale_b.name,
            "product_id": False,
            "account_id": cls.company_data["default_account_tax_sale"].id,
            "partner_id": cls.partner_a.id,
            "product_uom_id": False,
            "quantity": 1.0,
            "discount": 0.0,
            "price_unit": 30.0,
            "price_subtotal": 30.0,
            "price_total": 30.0,
            "tax_ids": [],
            "tax_line_id": cls.tax_sale_b.id,
            "currency_id": cls.company_data["currency"].id,
            "amount_currency": -30.0,
            "debit": 0.0,
            "credit": 30.0,
            "date_maturity": False,
            "tax_exigible": True,
        }

        cls.term_line_vals_1 = {
            "name": "",
            "product_id": False,
            "account_id": cls.company_data["default_account_receivable"].id,
            "partner_id": cls.partner_a.id,
            "product_uom_id": False,
            "quantity": 1.0,
            "discount": 0.0,
            "price_unit": -1410.0,
            "price_subtotal": -1410.0,
            "price_total": -1410.0,
            "tax_ids": [],
            "tax_line_id": False,
            "currency_id": cls.company_data["currency"].id,
            "amount_currency": 1410.0,
            "debit": 1410.0,
            "credit": 0.0,
            "date_maturity": fields.Date.from_string("2019-01-01"),
            "tax_exigible": True,
        }

        cls.move_vals = {
            "partner_id": cls.partner_a.id,
            "currency_id": cls.company_data["currency"].id,
            "journal_id": cls.company_data["default_journal_sale"].id,
            "date": fields.Date.from_string("2019-01-01"),
            "fiscal_position_id": False,
            "payment_reference": "",
            "invoice_payment_term_id": cls.pay_terms_a.id,
            "amount_untaxed": 1200.0,
            "amount_tax": 210.0,
            "amount_total": 1410.0,
        }

    #        cls.main_company = cls.env.ref("base.main_company")
    #        cls.company = cls.env.ref("l10n_br_base.empresa_lucro_presumido")
    #        cls.so_products = cls.env.ref("l10n_br_sale.lc_so_only_products")
    #        cls.so_services = cls.env.ref("l10n_br_sale.lc_so_only_services")
    #        cls.so_product_service = cls.env.ref("l10n_br_sale.lc_so_product_service")
    #        cls.fsc_op_sale = cls.env.ref("l10n_br_fiscal.fo_venda")
    #        # Testa os Impostos Dedutiveis
    #        cls.fsc_op_sale.deductible_taxes = True
    #        cls.fsc_op_line_sale = cls.env.ref("l10n_br_fiscal.fo_venda_venda")
    #        cls.fsc_op_line_sale_non_contr = cls.env.ref(
    #            "l10n_br_fiscal.fo_venda_venda_nao_contribuinte"
    #        )
    #        cls.fsc_op_line_resale = cls.env.ref("l10n_br_fiscal.fo_venda_revenda")
    #        cls.fsc_op_line_resale_non_contr = cls.env.ref(
    #            "l10n_br_fiscal.fo_venda_revenda_nao_contribuinte"
    #        )
    #        cls.fsc_op_line_serv_ind = cls.env.ref("l10n_br_fiscal.fo_venda_servico_ind")
    #        cls.fsc_op_line_serv = cls.env.ref("l10n_br_fiscal.fo_venda_servico")

    @classmethod
    def setup_company_data(cls, company_name, chart_template=None, **kwargs):
        if company_name == "company_1_data":
            company_name = "empresa 1 Simples Nacional"
        else:
            company_name = "empresa 2 Simples Nacional"
        chart_template = cls.env.ref(
            "l10n_br_coa_simple.l10n_br_coa_simple_chart_template"
        )
        res = super().setup_company_data(
            company_name,
            chart_template,
            tax_framework="1",
            is_industry=True,
#            simplified_tax_id=cls.env.ref("l10n_br_fiscal.simplefied_tax_anexo2").id,
#            simplified_tax_range_id=cls.env.ref("l10n_br_fiscal.simplefied_tax_anexo2_range4").id,
            coefficient_r=False,
            ripi=True,
            piscofins_id=cls.env.ref(
                "l10n_br_fiscal.tax_pis_cofins_simples_nacional"
            ).id,
            tax_ipi_id=cls.env.ref("l10n_br_fiscal.tax_ipi_outros").id,
            tax_icms_id=cls.env.ref("l10n_br_fiscal.tax_icms_sn_com_credito").id,
            cnae_main_id=cls.env.ref("l10n_br_fiscal.cnae_3101200").id,
            document_type_id=cls.env.ref("l10n_br_fiscal.document_55").id,
            annual_revenue=815000.0,
            **kwargs
        )
        return res

    def test_out_invoice_create_simp1(self):
        self.assertEqual(self.company_data["company"].simplifed_tax_id.name, "range")
 
    def test_out_invoice_create_simp2(self):
        self.assertEqual(self.company_data["company"].simplifed_tax_percent, 4)
 

    def test_out_invoice_create_ncm(self):
        self.assertEqual(self.company_data["company"].simplifed_tax_range_id.name, "range")
 

    def test_out_invoice_create_fiscal_taxes(self):
        self.assertEqual(self.invoice.invoice_line_ids[0].cfop_id.name, "blabla")
        self.assertEqual(self.invoice.invoice_line_ids[0].icmssn_tax_id, self.env.ref("l10n_br_fiscal.tax_icms_sn_com_credito"))
        self.assertEqual(self.invoice.invoice_line_ids[0].icms_cst_id, self.env.ref("l10n_br_fiscal.cst_icmssn_101"))
        self.assertEqual(self.invoice.invoice_line_ids[0].icmssn_percent, 2.70)
 
        self.assertEqual(self.invoice.invoice_line_ids[1].icmssn_tax_id, self.env.ref("l10n_br_fiscal.tax_icms_sn_com_credito"))
        self.assertEqual(self.invoice.invoice_line_ids[1].icms_cst_id, self.env.ref("l10n_br_fiscal.cst_icmssn_101"))

    def test_out_invoice_create_1(self):

        # we should verify fiscal lines values separately
        # as the comparation framework won't find them through the _inherits
#        self.assertEqual(self.invoice.invoice_line_ids[0].icmssn_tax_id, 42)
#        self.assertEqual(self.invoice.invoice_line_ids[0].fiscal_tax_ids, [])

        self.assertInvoiceValues(
            self.invoice,
            [
                {
                    **self.product_line_vals_1,
                    "currency_id": self.env.ref("base.BRL").id,
                    "amount_currency": -973.0,
                    "credit": 973.0,
                },
                {
                    **self.product_line_vals_2:,
                    "currency_id": self.env.ref("base.BRL").id,
                    "amount_currency": -973.0,
                    "credit": 973.0,
                },
                {
                    **self.tax_line_vals_1,
                    "currency_id": self.env.ref("base.BRL").id,
                    "amount_currency": -180.0,
                    "credit": 90.0,
                },
                {
                    **self.tax_line_vals_2,
                    "currency_id": self.env.ref("base.BRL").id,
                    "amount_currency": -30.0,
                    "credit": 15.0,
                },
                {
                    **self.term_line_vals_1,
                    "currency_id": self.env.ref("base.BRL").id,
                    "amount_currency": 1410.0,
                    "debit": 705.0,
                },
            ],
            {
                **self.move_vals,
                "currency_id": self.env.ref("base.BRL").id,
            },
        )
