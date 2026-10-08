import logging

from odoo import SUPERUSER_ID, api

logger = logging.getLogger(__name__)


def migrate(cr, version):
    """Clear stored declared values outside Argentine companies."""
    env = api.Environment(cr, SUPERUSER_ID, {})
    pickings = env["stock.picking"].search(
        [
            ("company_id.country_id.code", "!=", "AR"),
            ("declared_value", "!=", 0.0),
        ],
        order="id",
    )
    total = len(pickings)
    logger.info("Clearing stock.picking.declared_value for %s non-AR records", total)
    for offset in range(0, total, 1000):
        pickings[offset : offset + 1000].write({"declared_value": 0.0})
        env.flush_all()
        env.invalidate_all()
