# Copyright (C) 2018 - Magno Costa - Akretion
# Copyright (C) 2023 - TODAY Raphaël Valyi - Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from re import I
import mock

from odoo.addons.account.tests.common import AccountTestInvoicingCommon
from odoo.tests.common import tagged, Form, SingleTransactionCase, OdooSuite
from odoo.models import NewId, BaseModel


# This monkey patch is required to avoid triggering all the tests from
# TestAccountMoveOutInvoiceOnchanges when it is imported.
# see https://stackoverflow.com/questions/69091760/how-can-i-import-a-testclass-properly-to-inherit-from-without-it-being-run-as-a
def patched_addTest(self, test):
    # TODO call original_method, monkey patch properly
    # sanity checks
    if not callable(test):
        raise TypeError("{} is not callable".format(repr(test)))
    if isinstance(test, type) and issubclass(test,
                                             (case.TestCase, TestSuite)):
        raise TypeError("TestCases and TestSuites must be instantiated "
                        "before passing them to addTest()")
    if type(test).__name__ != "TestAccountMoveOutInvoiceOnchanges":
        self._tests.append(test)

original_addTest = OdooSuite.addTest
OdooSuite.addTest = patched_addTest

from odoo.addons.account.tests.test_account_move_out_invoice import TestAccountMoveOutInvoiceOnchanges

#OdooSuite.addTest = original_addTest


@tagged('post_install', '-at_install')
class TestCustomerInvoice(TestAccountMoveOutInvoiceOnchanges):
    """
    This is a simple test for ensuring l10n_br_account doesn't break the basic
    account module behavior with customer invoices.
    """

    @classmethod
    def setup_company_data(cls, company_name, chart_template=None, **kwargs):
        cls.env.user.groups_id |= cls.env.ref('l10n_br_fiscal.group_manager')
        return super().setup_company_data(company_name, chart_template, **kwargs)

    @classmethod
    def setUpClass(cls, chart_template_ref=None):
        super().setUpClass(chart_template_ref="l10n_generic_coa.configurable_chart_template")
#        super().setUpClass(chart_template_ref="l10n_br_coa_simple.l10n_br_coa_simple_chart_template")


# The following tests list is taken with
# cat addons/account/tests/test_account_move_out_invoice.py | grep "def test_"
# commented test are actually executed, just like when super() is called
# but may be calling super() is more explicit.
# disabled tests are overriden with the pass instruction.


#    def test_out_invoice_onchange_invoice_date(self):
#        pass

    def test_out_invoice_line_onchange_product_1(self):
        super().test_out_invoice_line_onchange_product_1()

    def test_out_invoice_line_onchange_product_2_with_fiscal_pos_1(self):
        super().test_out_invoice_line_onchange_product_2_with_fiscal_pos_1()

#    def test_out_invoice_line_onchange_product_2_with_fiscal_pos_2(self):
#        pass

    def test_out_invoice_line_onchange_business_fields_1(self):
        pass

    def test_out_invoice_line_onchange_accounting_fields_1(self):
        pass

#    def test_out_invoice_line_onchange_partner_1(self):
#        pass

#    def test_out_invoice_line_onchange_taxes_1(self):
#        pass

#    def test_out_invoice_line_onchange_rounding_price_subtotal_1(self):
#        pass

#    def test_out_invoice_line_onchange_rounding_price_subtotal_2(self):
#        pass

    def test_out_invoice_line_onchange_taxes_2_price_unit_tax_included(self):
        pass

#    def test_out_invoice_line_onchange_analytic(self):
#        pass

#    def test_out_invoice_line_onchange_analytic_2(self):
#        pass

#    def test_out_invoice_line_onchange_cash_rounding_1(self):
#        pass

#    def test_out_invoice_line_onchange_currency_1(self):
#        pass

    def test_out_invoice_line_tax_fixed_price_include_free_product(self):
        pass

    def test_out_invoice_line_taxes_fixed_price_include_free_product(self):
        pass

#    def test_out_invoice_create_refund(self):

#    def test_out_invoice_create_refund_multi_currency(self):

#    def test_out_invoice_create_refund_auto_post(self):

    def test_out_invoice_create_1(self):
        super().test_out_invoice_create_1()

#    def test_out_invoice_create_child_partner(self):
#    def test_out_invoice_write_1(self):
#    def test_out_invoice_write_2(self):
#    def test_out_invoice_post_1(self):
#    def test_out_invoice_post_2(self):
#    def test_out_invoice_switch_out_refund_1(self):
#    def test_out_invoice_switch_out_refund_2(self):
#    def test_out_invoice_reverse_move_tags(self):
#    def test_out_invoice_change_period_accrual_1(self):
#    def test_out_invoice_multi_date_change_period_accrual(self):

#    def test_out_invoice_filter_zero_balance_lines(self):

#    def test_out_invoice_recomputation_receivable_lines(self):

#    def test_out_invoice_rounding_recomputation_receivable_lines(self):

#    def test_out_invoice_multi_company(self):

#    def test_out_invoice_multiple_switch_payment_terms(self):
    def test_out_invoice_copy_custom_date(self):
         pass

#    def test_select_specific_product_account(self):

#    def test_out_invoice_note_and_tax_partner_is_set(self):
#    def test_out_invoice_reverse_caba(self):
    def test_out_invoice_duplicate_currency_rate(self):
        pass
#    def test_out_invoice_depreciated_account(self):
