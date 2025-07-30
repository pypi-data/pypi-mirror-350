from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class SubscriptionRequest(models.Model):
    _inherit = "subscription.request"
    _rec_name = "type"
    share_product_id = fields.Many2one(required=False)
    type = fields.Selection(
        selection_add=[("new", "New Cooperator"), ("sponsorship", "Sponsorship")]
    )

    sponsor_id = fields.Many2one(
        "res.partner",
        string="Sponsor",
        domain=lambda self: self._domain_sponsor_id(),
    )

    def _domain_sponsor_id(self):
        return [
            ("member", "=", True),
        ]

    def validate_subscription_request(self):
        try:
            invoice = super().validate_subscription_request()
        except UserError:
            if self.ordered_parts == 0 and self.type == "sponsorship":
                pass
            else:
                raise
        else:
            return invoice

        self._check_already_cooperator()

        if not self.partner_id:
            partner = self.create_coop_partner()
            self.partner_id = partner
        else:
            self.partner_id = self.partner_id[0]

        self.partner_id.cooperator = True

        self._create_company_contact()

        self.write({"state": "done"})
        return True

    def _check_already_cooperator(self):
        domain = False

        if self.already_cooperator:
            raise UserError(
                _(
                    "The checkbox already cooperator is"
                    " checked please select a cooperator."
                )
            )
        elif self.is_company and self.company_register_number:
            domain = [
                (
                    "company_register_number",
                    "=",
                    self.company_register_number,
                )
            ]
        elif not self.is_company and self.email:
            domain = [("email", "=", self.email)]

        if domain:
            self.partner_id = self.env['res.partner'].search(domain)

    def _create_company_contact(self):
        if self.is_company and not self.partner_id.has_representative():
            contact = False
            if self.email:
                domain = [("email", "=", self.email)]
                contact = self.env['res.partner'].search(domain)
                if contact:
                    contact.type = "representative"
            if not contact:
                contact_vals = self.get_representative_vals()
                self.env['res.partner'].create(contact_vals)
            else:
                if len(contact) > 1:
                    raise UserError(
                        _(
                            "There is two different persons with the"
                            " same national register number. Please"
                            " proceed to a merge before to continue"
                        )
                    )
                if contact.parent_id and contact.parent_id.id != self.partner_id.id:
                    raise UserError(
                        _(
                            "This contact person is already defined"
                            " for another company. Please select"
                            " another contact"
                        )
                    )
                else:
                    contact.write(
                        {"parent_id": self.partner_id.id, "representative": True}
                    )

    def get_partner_company_vals(self):
        values = super().get_partner_company_vals()
        values["sponsor_id"] = self.sponsor_id.id
        return values

    def get_partner_vals(self):
        values = super().get_partner_vals()
        values["sponsor_id"] = self.sponsor_id.id
        return values

    @api.constrains("share_product_id", "is_company")
    def _check_share_available_to_user(self):
        if self.share_product_id:
            super()._check_share_available_to_user()

    @api.constrains("sponsor_id")
    def _validate_sponsee_number(self):
        for sr in self:
            if sr.sponsor_id:
                sponsor = sr.sponsor_id
                if (
                    sponsor.active_sponsees_number
                    > sponsor.company_id.max_sponsees_number
                ):
                    raise ValidationError(_("Maximum number of sponsees exceeded"))
