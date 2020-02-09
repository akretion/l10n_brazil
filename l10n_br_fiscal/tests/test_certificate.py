# Copyright 2019 Akretion - Renato Lima <renato.lima@akretion.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from base64 import b64encode
from datetime import timedelta

from odoo import fields
from odoo.tests import common
from odoo.tools.misc import format_date
from OpenSSL import crypto


class TestCertificate(common.TransactionCase):
    def setUp(self):
        super().setUp()

        self.company_model = self.env["res.company"]
        self.certificate_model = self.env["l10n_br_fiscal.certificate"]
        self.company = self._create_compay()
        self._switch_user_company(self.env.user, self.company)

        self.cert_country = "BR"
        self.cert_issuer_a = "EMISSOR A TESTE"
        self.cert_issuer_b = "EMISSOR B TESTE"
        self.cert_subject_valid = "CERTIFICADO VALIDO TESTE"
        self.cert_date_exp = fields.Datetime.today() + timedelta(days=365)
        self.cert_subject_invalid = "CERTIFICADO INVALIDO TESTE"
        self.cert_passwd = "123456"
        self.cert_name = "{} - {} - {} - Valid: {}".format(
            "NF-E",
            "A1",
            self.cert_subject_valid,
            format_date(self.env, self.cert_date_exp),
        )

        # self.certificate_valid = self._create_certificate(
        #     valid=True, passwd=self.cert_passwd, issuer=self.cert_issuer_a,
        #     country=self.cert_country, subject=self.cert_subject_valid)
        #  self.certificate_invalid = self._create_certificate(
        #     valid=False, passwd=self.cert_passwd, issuer=self.cert_issuer_b,
        #     country=self.cert_country, subject=self.cert_subject_invalid)

    def _create_compay(self):
        # Creating a company
        company = self.env["res.company"].create(
            {
                "name": "Company Test Fiscal BR",
                "cnpj_cpf": "42.245.642/0001-09",
                "country_id": self.env.ref("base.br").id,
                "state_id": self.env.ref("base.state_br_sp").id,
            }
        )
        return company

    def _switch_user_company(self, user, company):
        """ Add a company to the user's allowed & set to current. """
        user.write(
            {
                "company_ids": [(6, 0, (company + user.company_ids).ids)],
                "company_id": company.id,
            }
        )

    def _create_certificate(
        self, valid=True, passwd=None, issuer=None, country=None, subject=None
    ):
        """Creating a fake certificate"""
        key = crypto.PKey()
        key.generate_key(crypto.TYPE_RSA, 2048)

        cert = crypto.X509()

        cert.get_issuer().C = country
        cert.get_issuer().CN = issuer

        cert.get_subject().C = country
        cert.get_subject().CN = subject

        cert.set_serial_number(2009)

        if valid:
            time_before = 0
            time_after = 365 * 24 * 60 * 60
        else:
            time_before = -1 * (365 * 24 * 60 * 60)
            time_after = 0

        cert.gmtime_adj_notBefore(time_before)
        cert.gmtime_adj_notAfter(time_after)
        cert.set_pubkey(key)
        cert.sign(key, "md5")

        p12 = crypto.PKCS12()
        p12.set_privatekey(key)
        p12.set_certificate(cert)

        return b64encode(p12.export(passwd))

    def test_valid_certificate(self):
        """Create and check a valid certificate"""
        cert = self.certificate_model.create(
            {
                "type": "nf-e",
                "subtype": "a1",
                "password": self.cert_passwd,
                "file": self._create_certificate(
                    valid=True,
                    passwd=self.cert_passwd,
                    issuer=self.cert_issuer_a,
                    country=self.cert_country,
                    subject=self.cert_subject_valid,
                ),
            }
        )

        self.assertEquals(cert.issuer_name, self.cert_issuer_a)
        self.assertEquals(cert.owner_name, self.cert_subject_valid)
        self.assertEquals(cert.date_expiration.year, self.cert_date_exp.year)
        self.assertEquals(cert.date_expiration.month, self.cert_date_exp.month)
        self.assertEquals(cert.date_expiration.day, self.cert_date_exp.day)
        self.assertEquals(cert.name, self.cert_name)

    # FIXME
    # def test_certificate_wrong_password(self):
    #     """Write a valid certificate with wrong password"""
    #     with self.assertRaises(ValidationError):
    #         self.cert.write({'password': '123454'})

    # def test_invalid_certificate(self):
    #     """Create and check a invalid certificate"""
    #     with self.assertRaises(ValidationError):
    #         cert = self.certificate_model.create({
    #             'type': 'nf-e',
    #             'subtype': 'a1',
    #             'password': self.cert_passwd,
    #             'file': self.certificate_invalid
    #         })
