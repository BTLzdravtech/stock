import logging

from odoo import SUPERUSER_ID, api

logger = logging.getLogger(__name__)


def migrate(cr, version):
    """Backfill picking_type_id in batches after making the related field stored."""
    env = api.Environment(cr, SUPERUSER_ID, {})
    lines = env["stock.move.line"].search([("picking_id", "!=", False)], order="id")
    total = len(lines)
    logger.info("Recomputing stock.move.line.picking_type_id for %s records", total)
    for offset in range(0, total, 1000):
        lines[offset : offset + 1000]._compute_picking_type_id()
        env.flush_all()
        env.invalidate_all()
