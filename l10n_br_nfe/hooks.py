# Copyright (C) 2019-2020 - Raphael Valyi Akretion
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import logging
import pkg_resources
import nfelib
from nfelib.v4_00 import leiauteNFe_sub as nfe_sub

from odoo import api, SUPERUSER_ID
from odoo.exceptions import ValidationError
from odoo.addons.spec_driven_model import hooks

_logger = logging.getLogger(__name__)


def pre_init_hook(cr):
    """
    The objective of this hook is to ensure the Brazil country is
    translated as "Brasil" in pt_BR to get the NFe tests pass
    even if the pt_BR language pack is not installed.
    """
    cr.execute("""SELECT id
    FROM ir_translation
    WHERE name='res.country,name' AND
    lang='pt_BR'""")
    if not cr.fetchone():
        cr.execute(
            """
            INSERT INTO ir_translation
            (name, res_id, lang, type, src, value, module, state)
            VALUES ('res.country,name', 31, 'pt_BR', 'model',
            'Brazil', 'Brasil', 'base', 'translated');
            """)


def post_init_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    hooks.register_hook(env, 'l10n_br_nfe',
                        'odoo.addons.l10n_br_nfe_spec.models.v4_00.leiauteNFe')

    hooks.post_init_hook(cr, registry, 'l10n_br_nfe',
                         'odoo.addons.l10n_br_nfe_spec.models.v4_00.leiauteNFe')
    cr.execute("select demo from ir_module_module where name='l10n_br_nfe';")
    is_demo = cr.fetchone()[0]
    if is_demo:
        res_items = ('..', 'tests',
                     'nfe', 'v4_00', 'leiauteNFe',
                     '35180803102452000172550010000474491454651420-nfe.xml')
        resource_path = "/".join(res_items)
        nfe_stream = pkg_resources.resource_stream(nfelib.__name__,
                                                   resource_path)

        # nfe_stream = pkg_resources.resource_stream('nfelib',
        # '../tests/nfe/v4_00/leiauteNFe/35180803102452000172550010000474491454651420-nfe.xml')
        nfe_binding = nfe_sub.parse(nfe_stream, silence=True)
        number = nfe_binding.infNFe.ide.nNF
        existing_nfes = env["l10n_br_fiscal.document"].search(
            [('number', '=', number)])

        try:
            existing_nfes.unlink()
            nfe = env["nfe.40.infnfe"].with_context(
                tracking_disable=True, edoc_type='in',
                lang='pt_BR').build(nfe_binding.infNFe)
            _logger.info(nfe.nfe40_emit.nfe40_CNPJ)
        except ValidationError:
            _logger.info("NF-e already %s imported by hooks" % (number,))
