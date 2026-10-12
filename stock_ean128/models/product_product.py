##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import api, models
from odoo.fields import Domain


class ProductProduct(models.Model):
    _inherit = "product.product"

    @api.model
    def _search_display_name(self, operator, value):
        domain = super()._search_display_name(operator, value)
        if not isinstance(value, str):
            return domain
        ean_value = value[1:] if value.startswith(" ") else value
        if not ean_value:
            return domain
        lot_domain = Domain("lot_ids", "any", Domain("ean_128", operator, ean_value))
        if operator in Domain.NEGATIVE_OPERATORS:
            return domain & lot_domain
        return domain | lot_domain

    @api.model
    def name_search(self, name="", domain=None, operator="ilike", limit=100):
        results = super().name_search(name, domain, operator, limit)
        if not name or operator in Domain.NEGATIVE_OPERATORS or (limit and len(results) >= limit):
            return results
        ean_name = name[1:] if name.startswith(" ") else name
        if not ean_name:
            return results
        product_domain = Domain(domain or Domain.TRUE)
        products = self.search_fetch(
            product_domain
            & Domain("id", "not in", [product_id for product_id, _display_name in results])
            & Domain("lot_ids", "any", Domain("ean_128", operator, ean_name)),
            ["display_name"],
            limit=limit - len(results) if limit else None,
        )
        return results + [(product.id, product.display_name) for product in products.sudo()]
