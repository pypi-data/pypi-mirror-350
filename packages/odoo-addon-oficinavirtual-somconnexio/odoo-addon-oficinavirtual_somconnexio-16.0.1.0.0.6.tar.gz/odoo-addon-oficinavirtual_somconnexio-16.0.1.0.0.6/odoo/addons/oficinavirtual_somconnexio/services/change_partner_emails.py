from odoo import _

from ..somoffice.user import SomOfficeUser


class ChangeSomofficeEmailService:
    def __init__(self, partner, email):
        self.partner = partner
        self.email = email

    def run(self):
        SomOfficeUser(
            self.partner.ref,
            "",
            self.partner.vat,
            "",
        ).change_email(self.email)
        self.partner.message_post(_("OV Email changed to {}").format(self.email))
        return True
