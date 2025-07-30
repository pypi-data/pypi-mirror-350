from odoo import models

from ..somoffice.user import SomOfficeUser


class ResPartner(models.Model):
    _inherit = "res.partner"

    def create_user(self, partner):
        SomOfficeUser(
            partner.ref,
            partner.email,
            partner.vat,
            partner.lang,
        ).create()
