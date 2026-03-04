import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)


@openupgrade.migrate()
def migrate(env, version):
    cr = env.cr

    _logger.info("START add vouchers to stock_move")
    openupgrade.add_columns(env, [
        ("stock.move", "vouchers", "char"),
    ])
    _logger.info("END add vouchers to stock_move")

    _logger.info("START add declared_value to stock_move")
    openupgrade.add_columns(env, [
        ("stock.move", "declared_value", "float"),
    ])
    _logger.info("END add declared_value to stock_move")