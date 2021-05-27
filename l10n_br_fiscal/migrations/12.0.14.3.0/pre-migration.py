# Copyright (C) 2021 - Raphaêl Valyi - Akretion
# License AGPL-3.0 or later (
# http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


_column_renames = {
    # l10n_br_fiscal/models/cest.py
    'fiscal_cest_ncm_rel': [
        ('l10n_br_fiscal_ncm_id', 'ncm_id'),
        ('l10n_br_fiscal_cest_id', 'cest_id'),
    ],

    # l10n_br_fiscal/models/nbm.py
    'fiscal_nbm_ncm_rel': [
        ('l10n_br_fiscal_ncm_id', 'ncm_id'),
        ('l10n_br_fiscal_nbm_id', 'nbm_id'),
    ],

    # l10n_br_fiscal/models/ncm_cest.py
    'fiscal_cest_ncm_rel': [
        ('l10n_br_fiscal_ncm_id', 'ncm_id'),
        ('l10n_br_fiscal_cest_id', 'cest_id'),
    ],

    # l10n_br_fiscal/models/simplified_tax.py
    # WTF FIXME!!!!!!!!!!!!
    'fiscal_simplified_tax_cnae_rel': [
        ('l10n_br_fiscal_simplified_tax_id', None),
        ('l10n_br_fiscal_cnae_id', None),
    ],

    # l10n_br_fiscal/models/ncm_nbm.py
    # TODO FIXME WTF ?????????????????????????????????? same as  l10n_br_fiscal/models/nbm.py before ?
    'fiscal_nbm_ncm_rel': [
        ('l10n_br_fiscal_ncm_id', 'ncm_id'),
        ('l10n_br_fiscal_nbm_id', 'nbm_id'),
    ],

    # l10n_br_fiscal/models/ncm_tax_pis_cofins.py
    'fiscal_pis_cofins_ncm_rel': [
        ('l10n_br_fiscal_ncm_id', None),
        ('l10n_br_fiscal_cest_id', None),
    ],

    # l10n_br_fiscal/models/res_company.py
    'res_company_fiscal_cnae_rel': [
        ('l10n_br_fiscal_simplified_tax_id', None),
        ('l10n_br_fiscal_cnae_id', None),
    ],


    # l10n_br_fiscal/models/tax_pis_cofins.py
    'fiscal_pis_cofins_ncm_rel': [
        ('l10n_br_fiscal_ncm_id', None),
        ('l10n_br_fiscal_nbm_id', None),
    ],

    # l10n_br_fiscal/models/tax_definition.py
    'tax_definition_state_to_rel': [
        ('l10n_br_fiscal_ncm_id', None),
        ('l10n_br_fiscal_cest_id', None),
    ],



    # l10n_br_fiscal/models/tax_definition.py
    'tax_definition_ncm_rel': [
        ('l10n_br_fiscal_simplified_tax_id', None),
        ('l10n_br_fiscal_cnae_id', None),
    ],
    # l10n_br_fiscal/models/tax_definition.py
    'tax_definition_cest_rel': [
        ('l10n_br_fiscal_ncm_id', None),
        ('l10n_br_fiscal_cest_id', None),
    ],

    # l10n_br_fiscal/models/tax_definition.py
    'tax_definition_nbm_rel': [
        ('l10n_br_fiscal_simplified_tax_id', None),
        ('l10n_br_fiscal_cnae_id', None),
    ],

    # l10n_br_fiscal/models/tax_definition.py
    'tax_definition_product_rel': [
        ('l10n_br_fiscal_simplified_tax_id', None),
        ('l10n_br_fiscal_cnae_id', None),
    ],
}


./l10n_br_account/models/account_tax_template.py-        relation='l10n_br_fiscal_account_template_tax_rel',
./l10n_br_account/models/account_tax.py-        relation='l10n_br_fiscal_account_tax_rel',

./l10n_br_fiscal/models/cest.py-        relation='fiscal_cest_ncm_rel',
./l10n_br_fiscal/models/nbm.py-        relation='fiscal_nbm_ncm_rel',
./l10n_br_fiscal/models/ncm_cest.py-        relation='fiscal_cest_ncm_rel',
./l10n_br_fiscal/models/simplified_tax.py-        relation='fiscal_simplified_tax_cnae_rel',
                 WTF ??????
./l10n_br_fiscal/models/ncm_nbm.py-        relation='fiscal_nbm_ncm_rel',
./l10n_br_fiscal/models/ncm_tax_pis_cofins.py-        relation='fiscal_pis_cofins_ncm_rel',
./l10n_br_fiscal/models/res_company.py-        relation="res_company_fiscal_cnae_rel",

./l10n_br_fiscal/models/tax_pis_cofins.py-        relation='fiscal_pis_cofins_ncm_rel',
./l10n_br_fiscal/models/tax_definition.py-        relation='tax_definition_state_to_rel',
./l10n_br_fiscal/models/tax_definition.py-        relation='tax_definition_ncm_rel',
./l10n_br_fiscal/models/tax_definition.py-        relation='tax_definition_cest_rel',
./l10n_br_fiscal/models/tax_definition.py-        relation='tax_definition_nbm_rel',
./l10n_br_fiscal/models/tax_definition.py-        relation='tax_definition_product_rel',


@openupgrade.migrate(use_env=True)
def migrate(env, version):
    openupgrade.rename_columns(cr, _column_renames)
