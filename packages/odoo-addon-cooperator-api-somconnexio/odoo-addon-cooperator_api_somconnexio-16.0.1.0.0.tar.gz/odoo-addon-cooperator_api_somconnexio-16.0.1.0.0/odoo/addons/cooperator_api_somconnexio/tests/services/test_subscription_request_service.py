import json
import odoo
from datetime import datetime, timedelta, date
from odoo.addons.base_rest_somconnexio.tests.common_service import BaseRestCaseAdmin
from odoo.addons.somconnexio.helpers.vat_normalizer import VATNormalizer
from ...services.subscription_request_process import SubscriptionRequestProcess


class SubscriptionRequestServiceRestCase(BaseRestCaseAdmin):
    def setUp(self):
        super().setUp()
        self.vals_subscription = {
            "name": "Manuel Dublues Test",
            "firstname": "Manuel",
            "lastname": "Dublues Test",
            "email": "manuel@demo-test.net",
            "address": {
                "street": "Fuenlabarada",
                "zip_code": "28943",
                "city": "Madrid",
                "country": "ES",
                "state": self.browse_ref("base.state_es_m").code,
            },
            "city": "Brussels",
            "zip_code": "1111",
            "country_id": self.ref("base.es"),
            "date": (datetime.now() - timedelta(days=12)).strftime("%Y-%m-%d"),
            "company_id": 1,
            "source": "manual",
            "lang": "ca_ES",
            "gender": "male",
            "birthdate": "1960-11-03",
            "iban": "ES6020808687312159493841",
            "vat": "49013933J",
            "nationality": "ES",
            "payment_type": "single",
            "discovery_channel_id": 1,
            "data_policy_approved": True,
            "financial_risk_approved": True,
            "generic_rules_approved": True,
            "internal_rules_approved": True,
        }
        self.url = "/api/subscription-request"

    def test_route_create_new_cooperator(self):
        cooperator_vals = self.vals_subscription.copy()
        cooperator_vals["type"] = "new"
        cooperator_vals["company_email"] = "company@example.org"

        response = self.http_post(self.url, data=cooperator_vals)
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content.decode("utf-8"))

        self.assertIn("id", content)
        sr = self.env["subscription.request"].search(
            [
                ("id", "=", content["id"]),
                ("name", "=", cooperator_vals["name"]),
            ]
        )

        self.assertEqual(sr.iban, cooperator_vals["iban"])
        self.assertEqual(
            sr.vat, VATNormalizer(cooperator_vals["vat"]).convert_spanish_vat()
        )
        self.assertEqual(sr.type, "new")
        self.assertEqual(sr.payment_type, cooperator_vals["payment_type"])
        self.assertEqual(sr.state_id.code, cooperator_vals["address"]["state"])
        self.assertEqual(
            sr.share_product_id.id,
            self.browse_ref(
                "cooperator_somconnexio.cooperator_share_product"
            ).product_variant_id.id,
        )
        self.assertEqual(sr.ordered_parts, 1)
        self.assertEqual(sr.gender, "male")
        self.assertEqual(sr.birthdate, date(1960, 11, 3))
        self.assertEqual(sr.firstname, cooperator_vals["firstname"])
        self.assertEqual(sr.lastname, cooperator_vals["lastname"])
        sr.validate_subscription_request()
        partner_id = sr.partner_id
        self.assertEqual(partner_id.state_id.code, cooperator_vals["address"]["state"])
        self.assertEqual(
            partner_id.country_id.code, cooperator_vals["address"]["country"]
        )
        self.assertEqual(partner_id.vat, "ES{}".format(cooperator_vals["vat"]))
        self.assertEqual(
            partner_id.bank_ids.acc_number.replace(" ", ""), cooperator_vals["iban"]
        )
        self.assertEqual(partner_id.nationality.code, cooperator_vals["nationality"])
        self.assertEqual(sr.source, "manual")

    def test_route_create_sponsorship(self):
        sponsored_vals = self.vals_subscription.copy()
        sponsored_vals["type"] = "sponsorship"
        sponsored_vals["company_email"] = "company@example.org"
        del sponsored_vals["source"]
        cooperator = self.env.ref("somconnexio.res_partner_2_demo")
        cooperator.company_id = self.env['res.company'].browse(1)
        sponsored_vals["sponsor_vat"] = cooperator.vat
        sponsored_vals.pop("iban")

        content = SubscriptionRequestProcess(self.env).create(**sponsored_vals)

        sr = self.env["subscription.request"].search(
            [
                ("id", "=", content["id"]),
                ("name", "=", sponsored_vals["name"]),
            ]
        )

        self.assertEqual(sr.sponsor_id.id, cooperator.id)
        self.assertFalse(sr.coop_agreement_id)
        self.assertEqual(sr.type, "sponsorship")
        self.assertEqual(sr.ordered_parts, 0)
        self.assertEqual(sr.source, "website")

    def test_route_create_sponsorship_coop_agreement(self):
        coop_agreement_vals = self.vals_subscription.copy()
        coop_agreement = self.env.ref("cooperator_somconnexio.coop_agreement_1_demo")
        coop_agreement_vals.update(
            {
                "type": "sponsorship_coop_agreement",
                "coop_agreement": coop_agreement.code,
                "source": "website_change_owner",
                "company_email": "company@example.org"
            }
        )

        response = self.http_post(self.url, data=coop_agreement_vals)
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content.decode("utf-8"))

        sr = self.env["subscription.request"].search(
            [
                ("id", "=", content["id"]),
                ("name", "=", coop_agreement_vals["name"]),
            ]
        )

        self.assertEqual(sr.coop_agreement_id, coop_agreement)
        self.assertEqual(sr.type, "sponsorship_coop_agreement")
        self.assertFalse(sr.sponsor_id)
        self.assertEqual(sr.ordered_parts, 0)
        self.assertEqual(sr.source, "website_change_owner")

    @odoo.tools.mute_logger("odoo.addons.base_rest.http")
    def test_route_create_sponsorship_coop_agreement_bad_code(self):
        coop_agreement_vals = self.vals_subscription.copy()
        coop_agreement_vals.update(
            {"type": "sponsorship_coop_agreement", "coop_agreement": "fake-code"}
        )

        response = self.http_post(self.url, data=coop_agreement_vals)
        self.assertEqual(response.status_code, 400)
        error_msg = response.json().get("description")
        self.assertRegex(error_msg, "Coop Agreement code fake-code not found")

    @odoo.tools.mute_logger("odoo.addons.base_rest.http")
    def test_route_create_bad_payment_type(self):
        cooperator_vals = self.vals_subscription.copy()
        cooperator_vals["type"] = "new"
        cooperator_vals["payment_type"] = "XXX"

        response = self.http_post(self.url, data=cooperator_vals)
        self.assertEqual(response.status_code, 400)
        error_msg = response.json().get("description")
        self.assertRegex(error_msg, "Payment type XXX not valid")

    @odoo.tools.mute_logger("odoo.addons.base_rest.http")
    def test_route_create_bad_nationality(self):
        cooperator_vals = self.vals_subscription.copy()
        cooperator_vals["type"] = "new"
        cooperator_vals["nationality"] = "XXX"

        response = self.http_post(self.url, data=cooperator_vals)
        self.assertEqual(response.status_code, 400)
        error_msg = response.json().get("description")
        self.assertRegex(error_msg, "Nationality XXX not found")

    @odoo.tools.mute_logger("odoo.addons.base_rest.http")
    def test_route_create_bad_state(self):
        cooperator_vals = self.vals_subscription.copy()
        cooperator_vals["type"] = "new"
        self.vals_subscription["address"]["state"] = "XXX"

        response = self.http_post(self.url, data=cooperator_vals)
        self.assertEqual(response.status_code, 400)

        error_msg = response.json().get("description")
        self.assertRegex(error_msg, "State XXX not found")

    @odoo.tools.mute_logger("odoo.addons.base_rest.http")
    def test_route_create_bad_source(self):
        cooperator_vals = self.vals_subscription.copy()
        cooperator_vals["type"] = "new"
        cooperator_vals["source"] = "XXX"

        url = "/api/subscription-request"
        response = self.http_post(url, data=cooperator_vals)
        self.assertEqual(response.status_code, 400)
        error_msg = response.json().get("description")
        self.assertRegex(error_msg, "source.+unallowed value XXX")

    def test_route_create_new_company_cooperator(self):
        cooperator_vals = self.vals_subscription.copy()
        cooperator_vals["type"] = "new"
        cooperator_vals["is_company"] = True
        cooperator_vals["company_name"] = "Manuel Coop"
        cooperator_vals["company_email"] = "manuel@example.org"
        del cooperator_vals["birthdate"]
        del cooperator_vals["gender"]

        content = SubscriptionRequestProcess(self.env).create(**cooperator_vals)

        self.assertIn("id", content)
        sr = self.env["subscription.request"].search(
            [
                ("id", "=", content["id"]),
                ("name", "=", cooperator_vals["company_name"]),
            ]
        )

        self.assertEqual(sr.company_email, cooperator_vals["company_email"])
