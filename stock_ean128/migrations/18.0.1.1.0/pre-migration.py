import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)


@openupgrade.migrate()
def migrate(env, version):
    cr = env.cr


    _logger.info("START add ean_128 to stock_lot")
    openupgrade.add_columns(env, [
        ("stock_lot", "ean_128", "char"),
    ])
    _logger.info("END add ean_128 to stock_lot")