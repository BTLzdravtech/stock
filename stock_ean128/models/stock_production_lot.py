##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import api, fields, models
from odoo.fields import Domain


class StockLot(models.Model):
    _inherit = "stock.lot"

    ean_128 = fields.Char(
        string="EAN128",
        compute="_compute_action_compute",
        store=True,
    )

    @api.depends("name", "product_id", "product_id.default_code")
    def _compute_action_compute(self):
        for rec in self:
            name = ""
            if rec.product_id.default_code:
                name += " 01 " + rec.product_id.default_code
            name += " 10 " + rec.name
            rec.ean_128 = name

    @api.model
    def _search_display_name(self, operator, value):
        domain = super()._search_display_name(operator, value)
        if not isinstance(value, str) or not value:
            return domain
        ean_domain = Domain("ean_128", operator, value)
        if operator in Domain.NEGATIVE_OPERATORS:
            return domain & ean_domain
        return domain | ean_domain

    @api.model
    def name_search(self, name="", domain=None, operator="ilike", limit=100):
        if not name or operator in Domain.NEGATIVE_OPERATORS:
            return super().name_search(name, domain, operator, limit)
        search_domain = Domain(domain or Domain.TRUE) & Domain("ean_128", operator, name)
        lots = self.search_fetch(search_domain, ["display_name"], limit=limit)
        if lots:
            return [(lot.id, lot.display_name) for lot in lots.sudo()]
        return super().name_search(name, domain, operator, limit)
