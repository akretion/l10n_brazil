# Copyright (C) 2021 - TODAY Renato Lima - Akretion
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openupgradelib import openupgrade


@openupgrade.migrate(use_env=True)
def migrate(env, version):
    openupgrade.update_module_names(
        env.cr,
        [('l10n_br_spec_nfe', 'l10n_br_nfe_spec')],
        merge_modules=True)
