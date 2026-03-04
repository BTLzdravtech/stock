import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)


@openupgrade.migrate()
def migrate(env, version):
    cr = env.cr

    _logger.info("START add removal_priority to stock_quant")
    openupgrade.add_columns(env, [
        ("stock.quant", "removal_priority", "integer"),
    ])

    openupgrade.logged_query(cr, """
        UPDATE stock_quant sq
           SET removal_priority = sl.removal_priority
          FROM stock_location sl
         WHERE sq.location_id = sl.id
           AND sq.removal_priority IS NULL
           AND sl.removal_priority IS NOT NULL
    """)

    _logger.info("END add removal_priority to stock_quant")