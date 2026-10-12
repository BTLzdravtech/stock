##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import api, fields, models


class StockRule(models.Model):
    _inherit = "stock.rule"

    propagate_carrier = fields.Boolean(compute="_compute_propagate_carrier", store=True, readonly=False)

    @api.depends("company_id.country_id", "picking_type_id.code")
    def _compute_propagate_carrier(self):
        """Make True by default if picking code is outgoing"""
        non_ar_rules = self.filtered(lambda rule: rule.company_id.country_id.code != "AR")
        non_ar_rules.propagate_carrier = False
        for rec in self - non_ar_rules:
            rec.propagate_carrier = rec.picking_type_id.code == "outgoing"
