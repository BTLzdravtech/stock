# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models


class AccountMove(models.Model):
    _inherit = "account.move"

    def button_create_landed_costs(self):
        """Use the inverse invoice rate only when the invoice provides one.

        Core handles every other case, including refund signs.
        """
        self.ensure_one()
        rate_to_use = self.inverse_invoice_currency_rate if "inverse_invoice_currency_rate" in self._fields else 0.0
        if not rate_to_use:
            return super().button_create_landed_costs()

        landed_costs_lines = self.line_ids.filtered("is_landed_costs_line")
        sign = -1 if self.move_type == "in_refund" else 1
        landed_costs = (
            self.env["stock.landed.cost"]
            .with_company(self.company_id)
            .create(
                {
                    "vendor_bill_id": self.id,
                    "cost_lines": [
                        (
                            0,
                            0,
                            {
                                "product_id": line.product_id.id,
                                "name": line.product_id.name,
                                "account_id": line.product_id.product_tmpl_id.get_product_accounts()[
                                    "stock_valuation"
                                ].id,
                                "price_unit": sign * line.price_subtotal * rate_to_use,
                                "split_method": line.product_id.split_method_landed_cost or "equal",
                            },
                        )
                        for line in landed_costs_lines
                    ],
                }
            )
        )
        action = self.env["ir.actions.actions"]._for_xml_id("stock_landed_costs.action_stock_landed_cost")
        return dict(action, view_mode="form", res_id=landed_costs.id, views=[(False, "form")])
