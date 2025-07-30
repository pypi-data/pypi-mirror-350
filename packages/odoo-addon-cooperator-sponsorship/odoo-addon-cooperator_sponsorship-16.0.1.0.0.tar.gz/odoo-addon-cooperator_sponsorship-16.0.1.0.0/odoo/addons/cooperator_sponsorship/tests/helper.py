from faker import Faker
from datetime import datetime, timedelta

faker = Faker("es_CA")


def subscription_request_create_data(odoo_env):
    return {
        "partner_id": 0,
        "already_cooperator": False,
        "is_company": False,
        "firstname": faker.first_name(),
        "lastname": faker.last_name(),
        "email": faker.email(),
        "ordered_parts": 1,
        "share_product_id": odoo_env.browse_ref(
            "cooperator.product_template_share_type_2_demo"
        ).product_variant_id.id,
        "address": faker.street_address(),
        "city": faker.city(),
        "zip_code": faker.postcode(),
        "country_id": odoo_env.ref("base.es"),
        "date": datetime.now() - timedelta(days=12),
        "company_id": 1,
        "source": "manual",
        "lang": "en_US",
        "sponsor_id": False,
        "iban": faker.iban(),
        "state": "draft",
    }
