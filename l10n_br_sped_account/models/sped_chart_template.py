# Copyright (C) 2020  Renato Lima - Akretion
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import _, api, fields, models
from odoo.exceptions import AccessError
from odoo.http import request
from odoo.tools import pycompat


class SpedChartTemplate(models.Model):
    _name = "l10n_br_sped_account.chart.template"
    _description = "SPED Chart of Account Template"

    name = fields.Char(
        string='Name',
        required=True)

    sped_account_ids = fields.One2many(
        comodel_name='l10n_br_sped_account.template',
        inverse_name='sped_chart_template_id',
        string='SPED Accounts Template',
        help='All SPED account template related.')

    def load_for_current_company(self):
        """Installs this chart of accounts on the current company."""
        self.ensure_one()
        # do not use `request.env` here, it can cause deadlocks
        if request and request.session.uid:
            current_user = self.env['res.users'].browse(request.uid)
            company = current_user.company_id
        else:
            # fallback to company of current user, most likely __system__
            # (won't work well for multi-company)
            company = self.env.user.company_id

        self = self.with_context(lang=company.partner_id.lang)
        if not self.env.user._is_admin():
            raise AccessError(
                _("Only administrators can load a charf of accounts"))

        existing_accounts = self.env['l10n_br_sped_account.account'].search(
            [('company_id', '=', company.id)])
        if existing_accounts:
            # we tolerate switching from sped accounting referential chart
            # as long as there isn't yet any accounting entries created
            # for the company.
            if self.env['account.chart.template'].existing_accounting(company):
                raise UserError(
                    _("Could not install new chart of account as there "
                      "are already accounting entries existing."))

            # delete sped account
            existing_accounts.unlink()

        company.write({'sped_chart_template_id': self.id})

        # Install sped account templates and generate the real objects
        acc_template_ref = self._install_template(company)

        return {}

    @api.multi
    def _install_template(self, company, acc_ref=None):
        """Recursively load the account template objects and create the real
           Objects from them.
        """
        self.ensure_one()
        if acc_ref is None:
            acc_ref = {}

        # Ensure, even if individually, that everything
        # is translated according to the company's language.
        tmp1 = self.with_context(
            lang=company.partner_id.lang)._load_template(
                company, account_ref=acc_ref)
        acc_ref.update(tmp1)
        return acc_ref

    @api.multi
    def _load_template(self, company, account_ref=None):
        """Generate SPED Account from the templates"""
        self.ensure_one()
        if account_ref is None:
            account_ref = {}

        # Generating Accounts from templates.
        account_template_ref = self.generate_sped_account(account_ref, company)
        account_ref.update(account_template_ref)

        return account_ref

    @api.multi
    def create_record_with_xmlid(self, company, template, model, vals):
        return self._create_records_with_xmlid(
            model, [(template, vals)], company).id

    def _create_records_with_xmlid(self, model, template_vals, company):
        """Create records for the given model name with the given vals, and
           create xml ids based on each record's template and company id.
        """
        if not template_vals:
            return self.env[model]
        template_model = template_vals[0][0]
        template_ids = [template.id for template, vals in template_vals]
        template_xmlids = template_model.browse(template_ids).get_external_id()
        data_list = []
        for template, vals in template_vals:
            module, name = template_xmlids[template.id].split('.', 1)
            xml_id = "%s.%s_%s" % (module, company.id, name)
            data_list.append(dict(xml_id=xml_id, values=vals, noupdate=True))
        return self.env[model]._load_records(data_list)

    def _get_account_values(self, company, account_template, account_parent_id):
        """This method generates a dictionary of all the values for the
           sped account that will be created.
        """
        self.ensure_one()

        values = {
            'code': account_template.code,
            'name': account_template.name,
            'account_type': account_template.account_type,
            'sped_type': account_template.sped_type,
            'level': account_template.level,
            'sped_table': account_template.sped_table,
            'parent_id': account_parent_id,
            'active': True,
            'note': account_template.note,
            'company_id': company.id,
        }
        return values

    @api.multi
    def generate_sped_account(self, acc_template_ref, company):
        self.ensure_one()
        account_tmpl_obj = self.env['l10n_br_sped_account.template']
        templates = account_tmpl_obj.search(
            [('nocreate', '!=', True),
             ('sped_chart_template_id', '=', self.id)],
            order='id')

        for template in templates:
            values = self._get_account_values(
                company, template, acc_template_ref.get(
                    template.parent_id.id, False))

            account = self.create_record_with_xmlid(
                company=company,
                template=template,
                model='l10n_br_sped_account.account',
                vals=values)

            acc_template_ref[template.id] = account

        return acc_template_ref
