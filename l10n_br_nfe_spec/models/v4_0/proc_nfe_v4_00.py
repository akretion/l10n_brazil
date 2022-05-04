# Copyright 2022 Akretion - Raphaël Valyi <raphael.valyi@akretion.com>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.en.html).
# Generated by https://github.com/akretion/xsdata-odoo
#
import textwrap
from odoo import fields, models

from .leiaute_nfe_v4_00 import TnfeProc

__NAMESPACE__ = "http://www.portalfiscal.inf.br/nfe"


class NfeProc(models.AbstractModel):
    "NF-e processada"
    _description = textwrap.dedent("    %s" % (__doc__,))
    _name = "nfe.40.nfeproc"
    _inherit = "spec.mixin.nfe"
    _binding_type = "NfeProc"
