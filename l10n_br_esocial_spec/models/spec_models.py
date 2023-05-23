# Copyright 2023-TODAY Akretion - Raphael Valyi <raphael.valyi@akretion.com>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.en.html).

from odoo import fields, models


class EsoSpecMixin(models.AbstractModel):
    _description = "Abstract Model"
    _name = "spec.mixin.eso"
    _field_prefix = "eso11_"
    _schema_name = "eso"
    _schema_version = "1.1.0"
    _odoo_module = "l10n_br_eso"
    _spec_module = (
        "odoo.addons.l10n_br_esocial_spec.models.v1_1.tipos.py"
    )
    _binding_module = "esociallib.esocial.bindings.v1_1.tipos.py" # TODO
    _spec_tab_name = "esocial"

    brl_currency_id = fields.Many2one(
        comodel_name="res.currency",
        string="Moeda",
        # FIXME compute method is better, but not working in v14.
        default=lambda self: self.env.ref("base.BRL"),
    )

    def _valid_field_parameter(self, field, name):
        if name in (
            "xsd_type",
            "xsd_required",
            "choice",
            "xsd_implicit",
            "xsd_choice_required",
        ):
            return True
        else:
            return super()._valid_field_parameter(field, name)
