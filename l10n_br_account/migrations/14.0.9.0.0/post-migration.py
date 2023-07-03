from openupgradelib import openupgrade


def migrate(cr, version):
    openupgrade.logged_query(
        cr,
        """
        ALTER TABLE account_move_line
        ALTER COLUMN fiscal_document_line_id DROP NOT NULL
        """,
    )
    openupgrade.logged_query(
        cr,
        """
        ALTER TABLE account_move
        ALTER COLUMN fiscal_document_id DROP NOT NULL
        """,
    )
    openupgrade.logged_query(
        cr,
        """
        UPDATE account_move_line
        SET fiscal_document_line_id = NULL
        WHERE move_id IN (
            SELECT id FROM account_move WHERE document_type IS NULL OR document_type = ''
        )
        OR exclude_from_invoice_tab = false
        """,
    )
    openupgrade.logged_query(
        cr,
        """
        UPDATE account_move
        SET fiscal_document_id = NULL
        WHERE document_type IS NULL OR document_type = ''
        """,
    )
