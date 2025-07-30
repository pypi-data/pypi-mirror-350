from mock import patch

from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError
from odoo.addons.cooperator.tests.cooperator_test_mixin import CooperatorTestMixin

from ..helper import subscription_request_create_data
from hashids import Hashids


class TestResPartner(TransactionCase, CooperatorTestMixin):
    def setUp(self, *args, **kwargs):
        self.set_up_cooperator_test_data()
        if not self.env.company.chart_template_id:
            # Load a CoA if there's none in current company
            coa = self.env.ref("l10n_generic_coa.configurable_chart_template", False)
            coa.try_loading(company=self.env.company, install_demo=False)
        super().setUp()
        self.partner = self.env['res.partner'].create({'name': 'Name'})
        self.partner.company_id = self.env['res.company'].browse(1)
        with patch(
            'hashids.Hashids.encode'
        ) as mock:
            mock.return_value = 'abcd'
            self.member = self.create_dummy_cooperator()
            self.member._compute_cooperative_membership_id()
            self.member.company_id = self.env['res.company'].browse(1)

    def test_hash_from_id_not_member_not_coop_candidate(self):
        with patch.object(
                Hashids, 'encode'
        ) as mock:
            mock.return_value = 'abcd'
            self.partner._compute_sponsorship_hash()
        self.assertFalse(self.partner.sponsorship_hash)

    def test_hash_from_id_member(self):
        with patch(
            'hashids.Hashids.encode'
        ) as mock:
            mock.return_value = 'abcd'
            self.member._compute_sponsorship_hash()
        self.assertEqual(self.member.sponsorship_hash, "ABCD")

    def test_hash_from_id_coop_candidate(self):
        sub_req = self.create_dummy_subscription_from_partner(self.partner)
        sub_req.validate_subscription_request()
        self.partner._compute_cooperative_membership_id()
        with patch(
            'hashids.Hashids.encode'
        ) as mock:
            mock.return_value = 'abcd'
            self.partner._compute_sponsorship_hash()
        self.assertTrue(self.partner.coop_candidate)
        self.assertEqual(self.partner.sponsorship_hash, "ABCD")

    def test_can_sponsor_coop_candidate_ok(self):
        sub_req = self.create_dummy_subscription_from_partner(self.partner)
        self.partner.company_id.max_sponsees_number = 5
        with patch(
                'odoo.addons.cooperator.models.subscription_request'
                '.SubscriptionRequest.setup_partner'
        ) as mock:
            mock.return_value = self.partner
            sub_req.validate_subscription_request()
            mock.assert_called()
        self.assertEqual(self.partner.company_id.max_sponsees_number, 5)
        cooperative_membership = (
            self.partner.get_create_cooperative_membership(self.partner.company_id)
        )
        self.assertTrue(cooperative_membership)
        self.assertEqual(cooperative_membership.partner_id, self.partner)
        self.assertEqual(sub_req.partner_id, self.partner)
        self.assertEqual(self.env.company.id, 1)
        self.assertEqual(self.env['cooperative.membership'].search([
            ('partner_id', '=', self.partner.id),
            ('company_id', '=', self.env.company.id)
        ]), cooperative_membership)
        self.assertEqual(
            self.partner.get_cooperative_membership(self.env.company),
            cooperative_membership
        )
        self.partner._compute_cooperative_membership_id()
        self.assertTrue(self.partner.cooperative_membership_id)
        self.assertTrue(self.partner.cooperative_membership_id.cooperator)
        self.assertTrue(self.partner.cooperator)
        self.assertTrue(self.partner.cooperative_membership_id.subscription_request_ids)
        self.assertEqual(
            self.partner.cooperative_membership_id.subscription_request_ids.state,
            "done"
        )
        self.assertFalse(
            self.partner.cooperative_membership_id.partner_id.sponsor_id
        )
        self.assertTrue(self.partner.coop_candidate)
        self.assertTrue(self.partner.can_sponsor())

    def test_can_sponsor_member_ok(self):
        self.assertTrue(self.member.can_sponsor())

    def test_can_sponsor_ko_max_number(self):
        self.assertTrue(self.member.can_sponsor())
        while (
            self.member.active_sponsees_number
            < self.member.company_id.max_sponsees_number
        ):
            sr_vals = subscription_request_create_data(self)
            sr_vals.update({"sponsor_id": self.member.id})
            self.assertTrue(self.env["subscription.request"].create(sr_vals))
        self.assertFalse(self.member.can_sponsor())
        sr_vals = subscription_request_create_data(self)
        sr_vals.update({"sponsor_id": self.member.id})
        self.assertRaises(
            ValidationError, self.env["subscription.request"].create, sr_vals
        )

    def test_active_number_sponsees(self):
        sponsored = self.env.ref("cooperator.res_partner_cooperator_4_demo")
        sponsor = self.env.ref("cooperator.res_partner_cooperator_2_demo")
        sponsor.company_id = self.env['res.company'].browse(1)
        sponsored.sponsor_id = sponsor

        self.assertEqual(sponsor.active_sponsees, [sponsored.name])
        self.assertEqual(sponsor.active_sponsees_number, 1)

        sr_vals = subscription_request_create_data(self)
        sr_vals.update({"sponsor_id": sponsor.id})
        new_sr = self.env["subscription.request"].create(sr_vals)

        self.assertEqual(sponsor.active_sponsees_number, 2)
        self.assertEqual(sponsor.active_sponsees, [sponsored.name, new_sr.name])

        sponsored.inactive_partner = True

        self.assertEqual(sponsor.active_sponsees_number, 1)
        self.assertEqual(sponsor.active_sponsees, [new_sr.name])
