import odoo

from odoo.addons.base_rest_somconnexio.tests.common_service import BaseRestCaseAdmin


class CRMLeadServiceRestCase(BaseRestCaseAdmin):
    def setUp(self):
        super().setUp()
        self.partner = self.env.ref("somconnexio.res_partner_1_demo")
        self.url = "/api/crm-lead"
        self.product_mobile = self.env.ref("somconnexio.150Min1GB")

        self.mbl_data = {
            "partner_id": self.partner.ref,
            "iban": "ES6621000418401234567891",
            "lead_line_ids": [
                {
                    "product_code": self.product_mobile.default_code,
                    "mobile_isp_info": {
                        "icc_donor": "123",
                        "phone_number": "123",
                        "type": "portability",
                        "delivery_address": {
                            "street": "123",
                            "zip_code": "08000",
                            "city": "Barcelona",
                            "country": "ES",
                            "state": "B",
                        },
                        "previous_provider": 1,
                        "previous_owner_name": "Newus",
                        "previous_owner_first_name": "Borgo",
                        "previous_owner_vat_number": "29461336S",
                        "previous_contract_type": "contract",
                    },
                    "broadband_isp_info": {},
                }
            ],
        }

    @odoo.tools.mute_logger("odoo.addons.base_rest.http")
    def test_route_bad_subscription_request_id_create(self):
        data = self.mbl_data.copy()
        data.pop("partner_id")
        data["subscription_request_id"] = 666

        response = self.http_post(self.url, data=data)
        self.assertEqual(response.status_code, 400)
        error_msg = response.json().get("description")
        self.assertRegex(error_msg, "SubscriptionRequest with id 666 not found")

    @odoo.tools.mute_logger("odoo.addons.base_rest.http")
    def test_route_bad_subcription_and_partner_ids(self):
        data = self.mbl_data.copy()
        data["subscription_request_id"] = (
            self.browse_ref("cooperator.subscription_request_1_demo").id,
        )

        response = self.http_post(self.url, data=data)

        self.assertEqual(response.status_code, 400)
