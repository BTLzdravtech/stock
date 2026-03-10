import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)


@openupgrade.migrate()
def migrate(env, version):
    cr = env.cr

    _logger.info("START add vouchers to stock_picking")
    openupgrade.add_columns(env, [
        ("stock_picking", "vouchers", "char"),
    ])
    _logger.info("END add vouchers to stock_picking")

    _logger.info("START add declared_value to stock_picking")
    openupgrade.add_columns(env, [
        ("stock_picking", "declared_value", "float"),
    ])
    _logger.info("END add declared_value to stock_picking")