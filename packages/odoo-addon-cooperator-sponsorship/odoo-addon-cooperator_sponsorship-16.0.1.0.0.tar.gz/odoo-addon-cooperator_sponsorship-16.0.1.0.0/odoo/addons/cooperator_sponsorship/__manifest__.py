{
    "name": "Odoo Sponsorship module for cooperator addon",
    "version": "16.0.1.0.0",
    "depends": ["cooperator", "l10n_generic_coa"],
    "external_dependencies": {
        "python": [
            "faker",
            "hashids",
            "stdnum",
        ],
    },
    "author": "Coopdevs Treball SCCL",
    "website": "https://coopdevs.org",
    "category": "Cooperative management",
    "summary": """
        Odoo Sponsorship module for cooperator addon.
    """,
    "license": "AGPL-3",
    "data": [
        "views/subscription_request_view.xml",
        "views/res_company_view.xml",
        "views/res_partner_view.xml",
        "wizards/sponsee_member_wizard.xml",
        "views/menus.xml",
    ],
}
