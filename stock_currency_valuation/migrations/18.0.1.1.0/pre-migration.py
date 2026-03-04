import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)


@openupgrade.migrate()
def migrate(env, version):
    cr = env.cr

    _logger.info("START add manual_currency_rate to stock_valuation_layer")
    openupgrade.add_columns(env, [
        ("stock.valuation.layer", "manual_currency_rate", "float"),
    ])
    _logger.info("END add manual_currency_rate to stock_valuation_layer")

    _logger.info("START add unit_cost_in_currency to stock_valuation_layer")
    openupgrade.add_columns(env, [
        ("stock.valuation.layer", "unit_cost_in_currency", "float"),
    ])
    _logger.info("END add unit_cost_in_currency to stock_valuation_layer")

    _logger.info("START add value_in_currency to stock_valuation_layer")
    openupgrade.add_columns(env, [
        ("stock.valuation.layer", "value_in_currency", "float"),
    ])
    _logger.info("END add value_in_currency to stock_valuation_layer")