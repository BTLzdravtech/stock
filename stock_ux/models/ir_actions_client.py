from odoo import models
from odoo.tools.safe_eval import safe_eval


class IRActionsClient(models.Model):
    _inherit = "ir.actions.client"

    def read(self, fields=None, load='_classic_read'):
        res = super().read(fields=fields, load=load)
        company = self.env.company
        if company and company.country_code:
            for i, action in enumerate(res):
                ctx = safe_eval(action.get("context") or "{}")
                ctx["company_country_code"] = company.country_code
                res[i]["context"] = ctx
        return res
