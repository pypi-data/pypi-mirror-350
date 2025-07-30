import json
from odoo.addons.base_rest_somconnexio.tests.common_service import BaseRestCaseAdmin
from odoo.addons.cooperator.tests.cooperator_test_mixin import CooperatorTestMixin
from ...services.res_partner_public_process import ResPartnerPublicProcess
from odoo.addons.component.tests.common import TransactionComponentRegistryCase


class TestResPartnerPublicService(
    BaseRestCaseAdmin, CooperatorTestMixin, TransactionComponentRegistryCase
):
    def setUp(self):
        super().setUp()
        self._setup_registry(self)
        self.url = "/public-api/partner/count"

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.set_up_cooperator_test_data()

    def test_route_count_one_member(self, *args):
        response = self.http_public_get(self.url)
        self.assertEqual(response.status_code, 200)
        decoded_response = json.loads(response.content.decode("utf-8"))
        self.assertIn("members", decoded_response)
        count_members = decoded_response["members"]
        self.Partner = self.env["res.partner"]
        self.subscription_request_1.iban = 'ES91 2100 0418 4502 0005 1332'
        self.subscription_request_1.vat = 'ES71127582J'
        self.subscription_request_1.country_id = self.ref('base.es')
        self.subscription_request_1.validate_subscription_request()
        self.pay_invoice(self.subscription_request_1.capital_release_request)
        decoded_response = ResPartnerPublicProcess(self.env).run_from_api()
        self.assertEqual(
            decoded_response,
            {"members": count_members + 1},
        )

    def test_route_count_one_coop_candidate(self, *args):
        response = self.http_public_get(self.url)
        self.assertEqual(response.status_code, 200)
        decoded_response = json.loads(response.content.decode("utf-8"))
        self.assertIn("members", decoded_response)
        count_members = decoded_response["members"]
        request = self.browse_ref(
            "cooperator_somconnexio.sc_subscription_request_1_demo"
        )

        request.validate_subscription_request()

        self.assertEqual(request.state, "done")
        self.assertTrue(request.partner_id)
        self.assertTrue(request.partner_id.coop_candidate)

        decoded_response = ResPartnerPublicProcess(self.env).run_from_api()
        self.assertEqual(
            decoded_response,
            {"members": count_members + 1},
        )

    def test_route_doesnt_count_one_partner_not_member(self, *args):
        response = self.http_public_get(self.url)
        self.assertEqual(response.status_code, 200)
        decoded_response = json.loads(response.content.decode("utf-8"))
        self.assertIn("members", decoded_response)
        count_members = decoded_response["members"]
        self.env['res.partner'].create(
            {
                "name": "test member",
                "is_customer": True,
            }
        )
        decoded_response = ResPartnerPublicProcess(self.env).run_from_api()
        self.assertEqual(
            decoded_response,
            {"members": count_members},
        )
