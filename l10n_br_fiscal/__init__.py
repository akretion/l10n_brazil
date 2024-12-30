# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from . import models
from . import wizards

import csv
from io import StringIO
import logging
import os
from odoo import SUPERUSER_ID, api
from odoo.tools import convert
from .demo import DEMO_NCM, DEMO_NBM, DEMO_NBS, DEMO_CEST

_logger = logging.getLogger(__name__)


# unlike regular data files: we will force noupdate=True for these files:
NOUPDATE_FILES = [
    "data/l10n_br_fiscal.cnae.csv",
    "data/l10n_br_fiscal.cfop.csv",
    "data/l10n_br_fiscal_cfop_data.xml",
    "data/l10n_br_fiscal.tax.ipi.control.seal.csv",
    "data/l10n_br_fiscal.tax.ipi.guideline.csv",
    "data/l10n_br_fiscal.tax.ipi.guideline.class.csv",
    "data/l10n_br_fiscal.tax.pis.cofins.base.csv",
    "data/l10n_br_fiscal.tax.pis.cofins.credit.csv",
    "data/l10n_br_fiscal.service.type.csv",
    "data/simplified_tax_data.xml",
    "data/operation_data.xml",
    "data/l10n_br_fiscal_tax_icms_data.xml",
]


def convert_csv_import(
    cr, module, fname, csvcontent, idref=None, mode="init", noupdate=False
):
    """
    This is a monkey patch allowing filtering for faster demo/test loading
    and allowing to force noupdate=True for some key fiscal data.
    """
    filename, _ext = os.path.splitext(os.path.basename(fname))
    model = filename.split("-")[0]
    if fname in NOUPDATE_FILES:
        noupdate = True

    # is is one of the very large fiscal data files?
    if model in (
        "l10n_br_fiscal.ncm",
        "l10n_br_fiscal.nbm",
        "l10n_br_fiscal.nbs",
        "l10n_br_fiscal.cest",
        # NOTE we could also speed up the cnae
        # if we also create a simplified demo/test simplified_tax.xml
    ):

        # now we will figure out if we are in demo/test mode
        # at this early stage of data module loading, the demo flag of the fiscal module
        # can still be False, that's why we will consider it's the demo/test mode
        # if the demo flag is set for the l10n_br_base module.
        env = api.Environment(cr, SUPERUSER_ID, {})
        modules = env["ir.module.module"].search(
            [("name", "in", ("l10n_br_base", "l10n_br_fiscal"))]
        )
        if any(module.demo for module in modules):
            # Then we will filter and load only the demo records:
            id_column_values = globals().get(f"DEMO_{model.split('.')[-1].upper()}")

            input_stream = StringIO(csvcontent.decode())
            output_stream = StringIO()

            # Read the CSV content
            csv_reader = csv.reader(input_stream)
            csv_writer = csv.writer(output_stream)

            # Write the header to the output
            header = next(csv_reader)
            csv_writer.writerow(header)

            # Filter and write rows matching the IDs
            line_count = 0
            for row in csv_reader:
                if row[0].replace('"', "") in id_column_values:
                    csv_writer.writerow(row)
                    line_count += 1

            _logger.info(
                f"(faster demo/test mode: loading only {line_count} demo lines)"
            )

            # Get the filtered content as a string
            output_stream.seek(0)
            csvcontent = output_stream.getvalue().encode()

    return convert.convert_csv_import._original_method(
        cr, module, fname, csvcontent, idref, mode, noupdate
    )


convert_csv_import._original_method = convert.convert_csv_import
convert.convert_csv_import = convert_csv_import
