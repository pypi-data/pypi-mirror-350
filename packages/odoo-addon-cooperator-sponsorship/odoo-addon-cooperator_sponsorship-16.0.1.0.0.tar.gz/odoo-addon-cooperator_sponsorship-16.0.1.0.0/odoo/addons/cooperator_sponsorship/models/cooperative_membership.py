from odoo import models, fields, api


class CooperativeMembership(models.Model):
    _inherit = "cooperative.membership"
    coop_candidate = fields.Boolean(compute='_compute_coop_candidate')

    @api.depends("member", "partner_id.subscription_request_ids.state")
    def _compute_coop_candidate(self):
        for record in self:
            if record.member:
                is_candidate = False
            else:
                sub_requests = record.subscription_request_ids.filtered(
                    lambda record: (
                        record.state == "done" and not record.partner_id.sponsor_id
                    )
                )
                is_candidate = bool(sub_requests)
            record.coop_candidate = is_candidate
