from odoo.tests.common import TransactionCase
from datetime import datetime, timedelta


class TestSubscription(TransactionCase):
    def setUp(self, *args, **kwargs):
        result = super().setUp(*args, **kwargs)
        self.env['res.company'].browse(1)._init_cooperator_data()
        if not self.env.company.chart_template_id:
            # Load a CoA if there's none in current company
            coa = self.env.ref("l10n_generic_coa.configurable_chart_template", False)
            coa.try_loading(company=self.env.company, install_demo=False)
        self.SubscriptionRequest = self.env["subscription.request"]
        self.vals_subscription = {
            "already_cooperator": False,
            "firstname": "Manuel",
            "lastname": "Dublues Test",
            "email": "manuel@demo-test.net",
            "ordered_parts": 1,
            "address": "schaerbeekstraat",
            "city": "Brussels",
            "zip_code": "1111",
            "country_id": 20,
            "date": datetime.now() - timedelta(days=12),
            "company_id": 1,
            "source": "manual",
            "share_product_id": None,
            "lang": "en_US",
        }
        return result

    def test_create_subscription_regular(self):
        vals_subscription_regular = self.vals_subscription.copy()
        self.product_template_test = self.browse_ref(
            "cooperator.product_template_share_type_1_demo"
        )
        vals_subscription_regular.update(
            {
                "share_product_id": self.product_template_test.product_variant_id.id,
                "ordered_parts": 1,
            }
        )
        subscription_regular = self.SubscriptionRequest.create(
            vals_subscription_regular
        )
        self.assertEqual(subscription_regular.subscription_amount, 50.0)

    def test_create_subscription_sponsorship(self):
        vals_subscription_sponsorship = self.vals_subscription.copy()
        sponsor_id = self.ref("cooperator.res_partner_cooperator_1_demo")
        self.env['res.partner'].browse(sponsor_id).company_id = (
            self.env['res.company'].browse(1)
        )
        vals_subscription_sponsorship.update(
            {
                "share_product_id": False,
                "ordered_parts": False,
                "type": "sponsorship",
                "sponsor_id": sponsor_id,
            }
        )
        subscription_regular = self.SubscriptionRequest.create(
            vals_subscription_sponsorship
        )
        self.assertEqual(subscription_regular.subscription_amount, 0.0)

    def test_validate_subscription_sponsorship(self):
        vals_subscription_sponsorship = self.vals_subscription.copy()
        sponsor_id = self.ref("cooperator.res_partner_cooperator_1_demo")
        self.env['res.partner'].browse(sponsor_id).company_id = (
            self.env['res.company'].browse(1)
        )
        vals_subscription_sponsorship.update(
            {
                "share_product_id": False,
                "ordered_parts": False,
                "sponsor_id": sponsor_id,
                "type": "sponsorship",
            }
        )

        subscription_sponsorship = self.SubscriptionRequest.create(
            vals_subscription_sponsorship
        )
        subscription_sponsorship.validate_subscription_request()

        partner = subscription_sponsorship.partner_id

        self.assertTrue(partner.cooperator)
        self.assertFalse(partner.member)
        self.assertEqual(partner.sponsor_id.id, sponsor_id)
        self.assertFalse(partner.coop_candidate)
        self.assertTrue(partner.coop_sponsee)
