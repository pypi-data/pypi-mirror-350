from odoo.addons.somconnexio.tests.sc_test_case import SCTestCase

from mock import patch


class TestResPartner(SCTestCase):
    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)
        self.parent_partner = self.env["res.partner"].create(
            {
                "name": "test",
                "vat": "ES00470223B",
                "country_id": self.ref("base.es"),
            }
        )

    @patch("odoo.addons.oficinavirtual_somconnexio.models.res_partner.SomOfficeUser")
    def test_create_user(self, mock_som_office_user):
        partner = self.parent_partner
        partner.create_user(partner)

        mock_som_office_user.assert_called_once_with(
            partner.ref,
            partner.email,
            partner.vat,
            partner.lang,
        )

        mock_som_office_user.return_value.create.assert_called_once()
