# Copyright (C) 2009 Renato Lima - Akretion <renato.lima@akretion.com.br>
# Copyright (C) 2014  KMEE - www.kmee.com.br
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import models, fields


class Cnae(models.Model):
    _name = 'fiscal.cnae'
    _description = 'CNAE'
    _inherit = 'fiscal.data.abstract'

    code = fields.Char(
        size=16)

    version = fields.Char(
        string='Version',
        size=16,
        required=True)

    parent_id = fields.Many2one(
        comodel_name='fiscal.cnae',
        string='Parent CNAE')

    child_ids = fields.One2many(
        comodel_name='fiscal.cnae',
        inverse_name='parent_id',
        string='Children CNAEs')

    internal_type = fields.Selection(
        selection=[('view', u'View'),
                   ('normal', 'Normal')],
        string='Internal Type',
        required=True,
        default='normal')

    _sql_constraints = [
        ('fiscal_cnae_code_uniq', 'unique (code)',
         'CNAE already exists with this code !')]
