# -*- coding: utf-8 -*-
# Copyright 2019 KMEE
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from __future__ import unicode_literals

from odoo import api, fields, models, _

PROCESSADOR = 'nenhum'


class ResCompany(models.Model):

    _inherit = 'res.company'

    processador_edoc = fields.Selection(
        selection=[(PROCESSADOR, 'Nenhum')],
        string='Processador documentos eletrônicos',
    )
    provedor_nfse = fields.Selection(
        selection=[
            ('ginfes', 'Ginfes'),
            ('dsf', 'DSF / Iss Digital'),
        ],
    )