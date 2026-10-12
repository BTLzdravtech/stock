import logging

from odoo import SUPERUSER_ID, api

logger = logging.getLogger(__name__)


def migrate(cr, version):
    """Recompute Argentine-only stored stock rule values."""
    env = api.Environment(cr, SUPERUSER_ID, {})
    rules = env["stock.rule"].search([("company_id.country_id.code", "!=", "AR")], order="id")
    total = len(rules)
    logger.info("Clearing stock.rule.propagate_carrier for %s non-AR records", total)
    for offset in range(0, total, 1000):
        rules[offset : offset + 1000]._compute_propagate_carrier()
        env.flush_all()
        env.invalidate_all()
