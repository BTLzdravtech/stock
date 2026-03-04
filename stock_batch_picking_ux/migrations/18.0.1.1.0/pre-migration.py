import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)


@openupgrade.migrate()
def migrate(env, version):
    cr = env.cr

    _logger.info("START add origin to stock_move_line")
    openupgrade.add_columns(env, [
        ("stock.move.line", "origin", "char"),
    ])

    openupgrade.logged_query(cr, """
        UPDATE stock_move_line sml
           SET origin = sp.origin
          FROM stock_move sm
          JOIN stock_picking sp ON sp.id = sm.picking_id
         WHERE sml.move_id = sm.id
           AND sml.origin IS NULL
           AND sp.origin IS NOT NULL
    """)

    _logger.info("END add origin to stock_move_line")