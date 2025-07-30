from datetime import datetime, timedelta
from odoo.tests.common import TransactionCase
from odoo.addons.cooperator.tests.cooperator_test_mixin import CooperatorTestMixin


class TestMemberWizard(TransactionCase, CooperatorTestMixin):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.set_up_cooperator_test_data()

    def setUp(self, *args, **kwargs):
        super().setUp()
        self.env['res.company'].browse(1)._init_cooperator_data()
        if not self.env.company.chart_template_id:
            # Load a CoA if there's none in current company
            coa = self.env.ref("l10n_generic_coa.configurable_chart_template", False)
            coa.try_loading(company=self.env.company, install_demo=False)

        self.SponseeMemberWizard = self.env["subscription.upgrade.sponsee"]
        sponsor_id = self.ref("cooperator.res_partner_cooperator_1_demo")
        self.env['res.partner'].browse(sponsor_id).company_id = (
            self.env['res.company'].browse(1)
        )
        vals_subscription_sponsorship = {
            "already_cooperator": False,
            "firstname": "Manuel",
            "lastname": "Dublues Test",
            "email": "manuel@demo-test.net",
            "ordered_parts": False,
            "address": "schaerbeekstraat",
            "city": "Brussels",
            "zip_code": "1111",
            "country_id": 20,
            "date": datetime.now() - timedelta(days=12),
            "company_id": 1,
            "source": "manual",
            "share_product_id": False,
            "lang": "en_US",
            "sponsor_id": sponsor_id,
            "type": "sponsorship",
            "iban": "ES10   00492352082414205416",
        }
        subscription_sponsorship = self.env["subscription.request"].create(
            vals_subscription_sponsorship
        )
        subscription_sponsorship.validate_subscription_request()
        self.sponsee = subscription_sponsorship.partner_id
        product_template = self.browse_ref(
            "cooperator.product_template_share_type_2_demo"
        )
        self.product = product_template.product_variant_id
        self.product.by_individual = True

    def test_sponsee_to_member_wizard_creation(self):
        wizard = self.SponseeMemberWizard.create(
            {"share_product_id": self.product.id, "partner_id": self.sponsee.id}
        )
        self.assertEqual(wizard.partner_id, self.sponsee)
        self.assertEqual(wizard.start_date, datetime.now().date())

    def test_sponsee_to_member_wizard_upgrade(self):
        wizard = self.SponseeMemberWizard.create(
            {"share_product_id": self.product.id, "partner_id": self.sponsee.id}
        )
        wizard.upgrade()

        self.assertTrue(self.sponsee.coop_candidate)
        self.assertFalse(self.sponsee.coop_sponsee)
