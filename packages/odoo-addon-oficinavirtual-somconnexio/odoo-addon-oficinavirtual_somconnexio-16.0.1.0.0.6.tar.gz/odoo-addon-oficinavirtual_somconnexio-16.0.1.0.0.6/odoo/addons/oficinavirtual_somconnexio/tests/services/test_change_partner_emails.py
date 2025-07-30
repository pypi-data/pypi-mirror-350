from mock import patch, Mock, ANY
import json
from odoo.addons.base_rest_somconnexio.tests.common_service import BaseRestCaseAdmin
from odoo.exceptions import UserError
from odoo.addons.res_partner_api_somconnexio.services.partner_email_change_process import (  # noqa
    PartnerEmailChangeProcess,
)
from ...services.change_partner_emails import ChangeSomofficeEmailService
from ...somoffice.errors import SomOfficeUserChangeEmailError


class TestPartnerEmailChangeService(BaseRestCaseAdmin):
    def setUp(self, *args, **kwargs):
        super().setUp()
        self.partner = self.browse_ref("base.partner_demo")
        self.partner.ref = "1234test"
        self.partner_ref = self.partner.ref
        self.email = "test@example.org"
        self.ResPartner = self.env["res.partner"]
        self.partner_email_b = self.ResPartner.create(
            {
                "name": "Email b",
                "email": self.email,
                "type": "contract-email",
                "parent_id": self.partner.id,
            }
        )

    @patch(
        "odoo.addons.oficinavirtual_somconnexio.wizards.partner_email_change.partner_email_change.ChangeSomofficeEmailService",  # noqa
        return_value=Mock(spec=["run"]),
    )
    def test_route_right_run_wizard_contact_email_change(
        self, MockChangeSomofficeEmailService
    ):
        url = "/public-api/partner-email-change"
        data = {
            "partner_id": self.partner_ref,
            "email": self.email,
        }
        response = self.http_public_post(url, data=data)
        self.assertEqual(response.status_code, 200)
        decoded_response = json.loads(response.content.decode("utf-8"))
        self.assertEqual(decoded_response, {"result": "OK"})
        self.env["partner.email.change.process"].run_from_api(**data)
        MockChangeSomofficeEmailService.assert_called_once_with(
            self.partner, self.partner_email_b.email
        )
        MockChangeSomofficeEmailService.return_value.run.assert_called_once_with()

    @patch(
        "odoo.addons.oficinavirtual_somconnexio.wizards.partner_email_change.partner_email_change.ChangeSomofficeEmailService",  # noqa
        return_value=Mock(spec=["run"]),
    )
    def test_route_bad_run_wizard_contact_email_fail(
        self, MockChangeSomofficeEmailService
    ):
        MockChangeSomofficeEmailService.return_value.run.side_effect = (
            SomOfficeUserChangeEmailError(self.partner.ref, "Error Text")
        )
        url = "/public-api/partner-email-change"
        data = {
            "partner_id": self.partner_ref,
            "email": self.email,
        }
        response = self.http_public_post(url, data=data)
        self.assertEqual(response.status_code, 200)
        decoded_response = json.loads(response.content.decode("utf-8"))
        self.assertEqual(decoded_response, {"result": "OK"})
        process = self.env["partner.email.change.process"]
        self.assertRaises(UserError, process.run_from_api, **data)

    @patch(
        "odoo.addons.oficinavirtual_somconnexio.services.change_partner_emails.SomOfficeUser",  # noqa
        return_value=Mock(spec=["change_email"]),
    )
    def test_run(self, MockSomOfficeUser):
        ChangeSomofficeEmailService(self.partner, self.partner_email_b.email).run()

        MockSomOfficeUser.assert_called_once_with(
            self.partner.ref,
            ANY,
            self.partner.vat,
            ANY,
        )
        MockSomOfficeUser.return_value.change_email.assert_called_once_with(
            self.partner_email_b.email,
        )
