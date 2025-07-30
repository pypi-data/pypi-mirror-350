import json
import odoo
from odoo.addons.base_rest_somconnexio.tests.common_service import BaseRestCaseAdmin


class TestCoopAgreementService(BaseRestCaseAdmin):
    def setUp(self):
        super().setUp()
        self.coop_agreement = self.browse_ref(
            "cooperator_somconnexio.coop_agreement_sc"
        )
        self.code = self.coop_agreement.code

    def test_search_coop_agreement_by_code(self):
        url = f"/api/coop-agreement/search?code={self.code}"

        response = self.http_get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.reason, "OK")

        content = json.loads(response.content.decode("utf-8"))

        expected_response = {
            "name": self.coop_agreement.partner_id.name,
            "code": self.code,
            "first_month_promotion": False,
        }

        self.assertEqual(content, expected_response)

    @odoo.tools.mute_logger("odoo.addons.base_rest.http")
    def test_search_coop_agreement_by_code_not_found(self):
        code = "invented"
        url = f"/api/coop-agreement/search?code={code}"

        response = self.http_get(url)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.reason, "NOT FOUND")

    def test_validator_return_search(self):
        url = f"/api/coop-agreement/search?code={self.code}"

        response = self.http_get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.reason, "OK")

        content = json.loads(response.content.decode("utf-8"))

        self.assertTrue(isinstance(content, dict))
        self.assertIn("name", content)
        self.assertIn("code", content)
        self.assertIsInstance(content["name"], str)
        self.assertIsInstance(content["code"], str)
