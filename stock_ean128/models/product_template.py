##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    lot_ids = fields.One2many(
        "stock.lot",
        compute="_compute_get_lots",
        search="_search_lots",
        string="Lots",
    )

    def _compute_get_lots(self):
        lots = self.env["stock.lot"].search([("product_id.product_tmpl_id", "in", self.ids)])
        lots_by_template = {}
        for lot in lots:
            lots_by_template.setdefault(lot.product_id.product_tmpl_id.id, self.env["stock.lot"])
            lots_by_template[lot.product_id.product_tmpl_id.id] |= lot
        for rec in self:
            rec.lot_ids = lots_by_template.get(rec.id, self.env["stock.lot"])

    def _search_lots(self, operator, operand):
        if isinstance(operand, str) and operand.startswith("\xa0"):
            operand = operand[1:]
        return [("product_variant_ids.lot_ids.ean_128", operator, operand)]
