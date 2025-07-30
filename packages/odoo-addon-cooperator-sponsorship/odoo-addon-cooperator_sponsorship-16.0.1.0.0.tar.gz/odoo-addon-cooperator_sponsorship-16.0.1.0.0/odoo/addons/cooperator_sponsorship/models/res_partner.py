from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from hashids import Hashids
import logging
import os

_logger = logging.getLogger(__name__)
HASH_LENGTH = 5


class ResPartner(models.Model):
    _inherit = "res.partner"

    sponsee_ids = fields.One2many(
        "res.partner", "sponsor_id", string="Sponsees", readonly=True
    )

    sponsor_id = fields.Many2one(
        "res.partner",
        string="Sponsor",
        domain=lambda self: self._domain_sponsor_id(),
    )

    coop_sponsee = fields.Boolean(
        string="Is Cooperator Sponsee?",
        compute="_compute_coop_sponsee",
        store=True,
        readonly=True,
    )

    sponsorship_hash = fields.Char(
        "Sponsorship Code",
        compute="_compute_sponsorship_hash",
        store=True,
        readonly=True,
    )

    # Inherit and overwrite default value if needed by the module logic
    inactive_partner = fields.Boolean(
        default=False,
        readonly=True,
    )

    def can_sponsor(self):
        """Return True if the partner can sponsor more partners."""
        self.ensure_one()
        _logger.info((
            "member {}, coop_candidate {}, "
            "company_id.max_sponsees_number {}"
        ).format(
            self.member, self.coop_candidate, self.company_id.max_sponsees_number
        ))
        return (
            self.member or self.coop_candidate
        ) and self.company_id.max_sponsees_number > self.active_sponsees_number

    @api.constrains("sponsor_id")
    def _validate_sponsee_number(self):
        for partner in self:
            if partner.sponsor_id:
                sponsor = partner.sponsor_id
                if (
                    sponsor.active_sponsees_number
                    > sponsor.company_id.max_sponsees_number
                ):
                    raise ValidationError(_("Maximum number of sponsees exceeded"))

    @property
    def active_sponsees(self):
        active_partner_sponsees = self.sponsee_ids.filtered(
            lambda x: not x.inactive_partner
        )
        active_sponsees_names = [sponsee.name for sponsee in active_partner_sponsees]
        new_sub_rqs = self.env["subscription.request"].search(
            [
                ("sponsor_id", "=", self.id),
                ("state", "=", "draft"),
            ]
        )
        new_sub_rqs_names = [sr.name for sr in new_sub_rqs]

        return active_sponsees_names + new_sub_rqs_names

    @api.depends(
        "cooperative_membership_id.member", "cooperative_membership_id.coop_candidate"
    )
    def _compute_sponsorship_hash(self):
        for partner in self:
            if (
                partner.member or partner.coop_candidate
            ) and not partner.sponsorship_hash:
                hash_base = Hashids(
                    min_length=HASH_LENGTH, salt=os.getenv("HASH_SALT", "")
                )
                partner.sponsorship_hash = hash_base.encode(partner.id).upper()

    @property
    def active_sponsees_number(self):
        return len(self.active_sponsees)

    def _domain_sponsor_id(self):
        return [
            "|",
            ("member", "=", True),
            ("coop_candidate", "=", True),
        ]

    @api.depends("sponsor_id")
    @api.depends("subscription_request_ids.state")
    def _compute_coop_candidate(self):
        for partner in self:
            if partner.member:
                is_candidate = False
            else:
                sub_requests = partner.subscription_request_ids.filtered(
                    lambda record: (record.state == "done" and not record.sponsor_id)
                )
                is_candidate = bool(sub_requests)
            partner.coop_candidate = is_candidate

    @api.depends("sponsor_id")
    def _compute_coop_sponsee(self):
        for partner in self:
            if partner.sponsor_id:
                partner.coop_sponsee = True
            else:
                partner.coop_sponsee = False
