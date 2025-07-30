import logging

from odoo import models, _
from odoo.exceptions import UserError
from ...services.change_partner_emails import ChangeSomofficeEmailService
from ...somoffice.errors import SomOfficeUserChangeEmailError

_logger = logging.getLogger(__name__)


class PartnerEmailChangeWizard(models.TransientModel):
    _inherit = "partner.email.change.wizard"

    def button_change(self):
        super().button_change()
        if self.change_contact_email == "yes":
            self._change_somoffice_email()

    def _change_somoffice_email(self):
        change_partner_somoffice_email = ChangeSomofficeEmailService(
            self.partner_id, self.email_id.email
        )
        try:
            change_partner_somoffice_email.run()
        except SomOfficeUserChangeEmailError as error:
            _logger.error(error)
            msg = _(
                "Couldn't change SomOffice user email. "
                + "Please contact IT department"
            )
            raise UserError(msg)
        return True
