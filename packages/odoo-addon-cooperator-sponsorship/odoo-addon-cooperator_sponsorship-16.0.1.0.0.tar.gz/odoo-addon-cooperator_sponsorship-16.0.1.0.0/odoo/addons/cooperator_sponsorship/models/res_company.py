from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    max_sponsees_number = fields.Integer(string="Max Sponsees Number", default=5)
