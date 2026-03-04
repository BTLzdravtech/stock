import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)


@openupgrade.migrate()
def migrate(env, version):
    cr = env.cr

    _logger.info("START add picking_type_id to stock_move_line")
    openupgrade.add_columns(env, [
        ("stock.move.line", "picking_type_id", "many2one"),
    ])

    openupgrade.logged_query(cr, """
        UPDATE stock_move_line sml
           SET picking_type_id = sp.picking_type_id
          FROM stock_picking sp
         WHERE sml.picking_id = sp.id
           AND sml.picking_type_id IS NULL
           AND sp.picking_type_id IS NOT NULL
    """)

    _logger.info("END add picking_type_id to stock_move_line")