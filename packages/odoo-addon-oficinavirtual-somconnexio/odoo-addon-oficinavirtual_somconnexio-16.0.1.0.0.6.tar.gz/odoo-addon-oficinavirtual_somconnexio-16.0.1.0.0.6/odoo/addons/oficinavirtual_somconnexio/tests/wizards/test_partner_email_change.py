from mock import patch, Mock
from datetime import date

from odoo.exceptions import UserError

from odoo.addons.somconnexio.tests.sc_test_case import SCTestCase
from odoo.addons.somconnexio.tests.helper_service import contract_fiber_create_data
from ...somoffice.errors import SomOfficeUserChangeEmailError


class TestPartnerEmailChangeWizard(SCTestCase):
    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)
        self.vodafone_fiber_contract_service_info = self.env[
            "vodafone.fiber.service.contract.info"
        ].create(
            {
                "phone_number": "654321123",
                "vodafone_id": "123",
                "vodafone_offer_code": "456",
            }
        )
        self.partner = self.env.ref("somconnexio.res_partner_2_demo")
        vals_contract = contract_fiber_create_data(self.env, self.partner)
        self.Contract = self.env["contract.contract"]
        self.contract = self.Contract.create(vals_contract)
        vals_contract_same_partner = vals_contract.copy()
        vals_contract_same_partner.update({"name": "Test Contract Broadband B"})
        self.contract_same_partner = self.Contract.create(vals_contract_same_partner)
        self.partner_email_b = self.env["res.partner"].create(
            {
                "name": "Email b",
                "email": "email_b@example.org",
                "type": "contract-email",
                "parent_id": self.env.ref("somconnexio.res_partner_2_demo").id,
            }
        )
        self.user_admin = self.browse_ref("base.user_admin")
        self.expected_activity_args = {
            "res_model_id": self.env.ref("contract.model_contract_contract").id,
            "user_id": self.user_admin.id,
            "activity_type_id": self.env.ref(
                "somconnexio.mail_activity_type_contract_data_change"
            ).id,  # noqa
            "date_done": date.today(),
            "date_deadline": date.today(),
            "summary": "Email change",
            "done": True,
        }

    @patch(
        "odoo.addons.oficinavirtual_somconnexio.wizards.partner_email_change.partner_email_change.ChangeSomofficeEmailService",  # noqa
        return_value=Mock(spec=["run"]),
    )
    def test_change_contact_email_updating_somoffice_email(
        self, MockChangeSomofficeEmailService
    ):
        wizard = (
            self.env["partner.email.change.wizard"]
            .with_context(active_id=self.partner.id)
            .with_user(self.user_admin)
            .create(
                {
                    "change_contact_email": "yes",
                    "change_contracts_emails": "no",
                    "email_id": self.partner_email_b.id,
                }
            )
        )

        wizard.button_change()

        MockChangeSomofficeEmailService.assert_called_once_with(
            self.partner, self.partner_email_b.email
        )
        MockChangeSomofficeEmailService.return_value.run.assert_called_once_with()

    @patch(
        "odoo.addons.oficinavirtual_somconnexio.wizards.partner_email_change.partner_email_change.ChangeSomofficeEmailService",  # noqa
        return_value=Mock(spec=["run"]),
    )
    def test_change_contact_email_fail_updating_somoffice_email(
        self, MockChangeSomofficeEmailService
    ):
        MockChangeSomofficeEmailService.return_value.run.side_effect = (
            SomOfficeUserChangeEmailError(self.partner.ref, "Error Text")  # noqa
        )

        wizard = (
            self.env["partner.email.change.wizard"]
            .with_context(active_id=self.partner.id)
            .with_user(self.user_admin)
            .create(
                {
                    "change_contact_email": "yes",
                    "change_contracts_emails": "no",
                    "email_id": self.partner_email_b.id,
                }
            )
        )

        with self.assertRaises(UserError):
            wizard.button_change()
