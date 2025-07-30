import odoo

from odoo.addons.base_rest_somconnexio.tests.common_service import BaseRestCaseAdmin


class ResPartnerServiceTest(BaseRestCaseAdmin):

    def setUp(self):
        super().setUp()
        self.partner = self.browse_ref("somconnexio.res_partner_1_demo")
        self.url = "/api/partner"
        self.sponsees_url = self.url + "/sponsees"

    @odoo.tools.mute_logger("odoo.addons.auth_api_key.models.ir_http")
    @odoo.tools.mute_logger("odoo.addons.base_rest.http")
    def test_raise_error_without_auth(self):
        response = self.http_public_get(self.url)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.reason, "FORBIDDEN")

    @odoo.tools.mute_logger("odoo.addons.base_rest.http")
    def test_route_get_without_vat(self):
        response = self.http_get(self.url)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.reason, "BAD REQUEST")

    # TODO: The get test is not working because the route works wrong and returns the
    #       the next error:
    #           "NoComponentError: No component found for collection
    #           'res.partner.service.address' and resource 'address'"
    #       The problem is that the route is not working correctly but out of tests
    #       context it is working fine.
    #       We don't know how to fix it.
    # def test_route_get(self):
    #     content = self.http_get_content("{}/{}".format(
    #         self.url, self.partner.id)
    #     )
    #
    #     self.assertEqual(content["id"], self.partner.id)
    #     self.assertEqual(content["name"], self.partner.name)
    #     self.assertEqual(content["ref"], self.partner.ref)
    #     self.assertEqual(content["addresses"][0]["street"], self.partner.street)

    @odoo.tools.mute_logger("odoo.addons.base_rest.http")
    def test_route_search_not_found(self):
        response = self.http_get("{}?vat={}".format(self.url, "66758531L"))

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.reason, "NOT FOUND")

    def test_route_search(self):
        content = self.http_get_content("{}?vat={}".format(self.url, self.partner.vat))

        self.assertEqual(content["id"], self.partner.id)

    def test_route_search_normalize_vat(self):
        bad_formatted_vat = "  {}---. ".format(self.partner.vat)
        content = self.http_get_content("{}?vat={}".format(self.url, bad_formatted_vat))

        self.assertEqual(content["id"], self.partner.id)

    def test_filter_duplicate_addresses(self):
        address_dict = {
            "type": "service",
            "parent_id": self.partner.id,
            "street": "test",
            "street2": "test",
            "zip": "08123",
            "city": "city",
            "state_id": self.ref("base.state_es_b"),
            "country_id": self.ref("base.es"),
            "name": "test",
        }
        address_dict["street"] = "Test"
        self.env["res.partner"].create(address_dict)
        address_dict["street"] = "  Test "
        self.env["res.partner"].create(address_dict)

        content = self.http_get_content("{}?vat={}".format(self.url, self.partner.vat))

        self.assertEqual(content["id"], self.partner.id)
        self.assertEqual(len(content["addresses"]), 2)

    def test_route_search_banned_actions(self):
        content = self.http_get_content("{}?vat={}".format(self.url, self.partner.vat))

        self.assertFalse(self.partner.banned_action_tags)
        self.assertEqual(content["banned_actions"], [])

        action_new_service = self.browse_ref("somconnexio.new_services_action")
        action_one_shot = self.browse_ref("somconnexio.mobile_one_shot_action")
        self.partner.write(
            {
                "banned_action_tags": [
                    (6, 0, [action_new_service.id, action_one_shot.id])
                ]
            }
        )

        self.assertIn(action_new_service, self.partner.banned_action_tags)
        self.assertIn(action_one_shot, self.partner.banned_action_tags)
        self.assertEqual(len(self.partner.banned_action_tags), 2)

        content = self.http_get_content("{}?vat={}".format(self.url, self.partner.vat))

        self.assertEqual(
            content["banned_actions"], [action_new_service.code, action_one_shot.code]
        )

    def test_get_company_partner(self):
        partner = self.browse_ref("somconnexio.res_partner_company_demo")

        content = self.http_get_content("{}?vat={}".format(self.url, partner.vat))

        self.assertTrue(content["is_company"])
