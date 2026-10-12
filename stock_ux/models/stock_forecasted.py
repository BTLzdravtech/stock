from odoo import api, models
from odoo.exceptions import AccessError


class StockForecasted(models.AbstractModel):
    _inherit = "stock.forecasted_product_product"

    @api.model
    def action_unreserve_linked_picks(self, move_id):
        move = self.env["stock.move"].browse(move_id)
        if move.company_id.country_id.code != "AR":
            return super().action_unreserve_linked_picks(move_id)
        if self.env.user.has_group("stock_ux.group_restrict_to_modify_reservations_from_planned"):
            raise AccessError("You are not allowed to unreserve stock.")
        return super().action_unreserve_linked_picks(move_id)

    @api.model
    def action_reserve_linked_picks(self, move_id):
        move = self.env["stock.move"].browse(move_id)
        if move.company_id.country_id.code != "AR":
            return super().action_reserve_linked_picks(move_id)
        if self.env.user.has_group("stock_ux.group_restrict_to_modify_reservations_from_planned"):
            raise AccessError("You are not allowed to reserve stock.")
        return super().action_reserve_linked_picks(move_id)
