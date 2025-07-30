from unittest.mock import patch
from odoo.addons.somconnexio.tests.sc_test_case import SCTestCase
from odoo.exceptions import AccessError


class TestPartnerCheckSomofficeEmailWizard(SCTestCase):
    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)
        self.partner = self.browse_ref("somconnexio.res_partner_2_demo")

    @patch(
        "odoo.addons.oficinavirtual_somconnexio.somoffice.user.SomOfficeUser.get",
        autospec=True,
    )  # noqa
    def test_get_somoffice_email_ok(self, mock_somoffice_user_get):
        expected_somoffice_user_info = {
            "vat": self.partner.vat,
            "email": "user@somoffice.cat",
            "lang": "es_ES",
        }

        def _side_effect_somoffice_get(vat):
            if vat == self.partner.vat:
                return expected_somoffice_user_info

        mock_somoffice_user_get.side_effect = _side_effect_somoffice_get

        wizard = (
            self.env["partner.check.somoffice.email.wizard"]
            .with_context(active_id=self.partner.id)
            .create({})
        )

        wizard._compute_somoffice_email()

        self.assertEqual(wizard.partner_id, self.partner)
        self.assertEqual(
            wizard.somoffice_email, expected_somoffice_user_info.get("email")
        )

    @patch(
        "odoo.addons.oficinavirtual_somconnexio.somoffice.user.SomOfficeUser.get",
        autospec=True,
    )  # noqa
    def test_get_somoffice_email_user_not_found(self, mock_somoffice_user_get):
        def _side_effect_somoffice_get(vat):
            if vat == self.partner.vat:
                return {"msg": "error"}

        mock_somoffice_user_get.side_effect = _side_effect_somoffice_get

        with self.assertRaises(AccessError):
            wizard = (
                self.env["partner.check.somoffice.email.wizard"]
                .with_context(active_id=self.partner.id)
                .create({})
            )
            wizard._compute_somoffice_email()
