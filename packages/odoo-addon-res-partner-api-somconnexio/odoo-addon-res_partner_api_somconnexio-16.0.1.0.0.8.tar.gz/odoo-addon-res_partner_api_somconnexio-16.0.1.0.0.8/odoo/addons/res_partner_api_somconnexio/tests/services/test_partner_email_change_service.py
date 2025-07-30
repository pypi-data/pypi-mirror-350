from mock import patch
import json
from odoo.addons.base_rest_somconnexio.tests.common_service import BaseRestCaseAdmin
from odoo.exceptions import UserError


class PartnerEmailChangeServiceTest(BaseRestCaseAdmin):
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
        self.PartnerEmailChangeProcess = self.env["partner.email.change.process"]

    @patch(
        "odoo.addons.somconnexio.models.change_partner_emails.ChangePartnerEmails.change_contact_email",  # noqa
    )
    def test_route_right_run_wizard_contact_email_change(
        self, mock_change_contact_email
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
        self.PartnerEmailChangeProcess.run_from_api(**data)
        mock_change_contact_email.assert_called_once_with(  # noqa
            self.partner,
            self.partner_email_b,
        )

    def test_route_bad_run_wizard_missing_partner_id(self):
        url = "/public-api/partner-email-change"
        data = {
            "email": self.email,
        }
        response = self.http_public_post(url, data=data)
        self.assertEqual(response.status_code, 200)
        decoded_response = json.loads(response.content.decode("utf-8"))
        self.assertEqual(decoded_response, {"result": "OK"})

        self.assertRaises(
            UserError, self.PartnerEmailChangeProcess.run_from_api, **data
        )

    def test_route_bad_run_wizard_missing_email(self):
        url = "/public-api/partner-email-change"
        data = {
            "partner_id": self.partner_ref,
            "change_contracts_emails": False,
            "change_contact_email": True,
        }
        response = self.http_public_post(url, data=data)
        self.assertEqual(response.status_code, 200)
        decoded_response = json.loads(response.content.decode("utf-8"))
        self.assertEqual(decoded_response, {"result": "OK"})
        self.assertRaises(
            UserError, self.PartnerEmailChangeProcess.run_from_api, **data
        )

    def test_route_bad_run_wizard_partner_id_not_found(self):
        url = "/public-api/partner-email-change"
        data = {
            "partner_id": "XXX",
            "email": self.email,
            "change_contracts_emails": False,
            "change_contact_email": True,
        }
        response = self.http_public_post(url, data=data)
        self.assertEqual(response.status_code, 200)
        decoded_response = json.loads(response.content.decode("utf-8"))
        self.assertEqual(decoded_response, {"result": "OK"})
        self.assertRaises(
            UserError, self.PartnerEmailChangeProcess.run_from_api, **data
        )
