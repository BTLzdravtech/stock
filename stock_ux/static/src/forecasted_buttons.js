/** @odoo-module **/
import { ForecastedButtons } from "@stock/stock_forecasted/forecasted_buttons";
import { patch } from "@web/core/utils/patch";
import { user } from "@web/core/user";
import { useState } from "@odoo/owl";

patch(ForecastedButtons.prototype, {
    setup() {
        super.setup(...arguments);
        this.movementsState = useState({ visible: false });
        this._loadMovementsVisibility();
    },

    async _loadMovementsVisibility() {
        const [company] = await this.orm.read("res.company", [user.activeCompany.id], ["country_code"]);
        this.movementsState.visible = company?.country_code === "AR";
    },

    async _onClickTrace() {
        const action = await this.actionService.loadAction("stock.stock_move_action");
        const field = this.resModel === "product.product" ? "product_id" : "product_id.product_tmpl_id";
        action.domain = [[field, "=", this.productId]];
        action.context = {
            ...action.context,
            search_default_future: 1,
            search_default_picking_type: 1,
        };
        return this.actionService.doAction(action);
    },
});
