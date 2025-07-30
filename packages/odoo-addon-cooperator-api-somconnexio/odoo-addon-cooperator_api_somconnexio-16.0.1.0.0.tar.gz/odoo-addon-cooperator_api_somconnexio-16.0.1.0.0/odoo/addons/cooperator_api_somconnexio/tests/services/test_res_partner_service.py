import json
from odoo.addons.cooperator.tests.cooperator_test_mixin import CooperatorTestMixin
from odoo.addons.base_rest_somconnexio.tests.common_service import BaseRestCaseAdmin
from odoo.addons.somconnexio.tests.helper_service import crm_lead_create
from odoo.addons.cooperator_sponsorship.tests.helper import (
    subscription_request_create_data,
)
from ...services.res_partner_process import ResPartnerProcess


class TestResPartnerService(BaseRestCaseAdmin, CooperatorTestMixin):
    def setUp(self):
        super().setUp()
        self.partner = self.browse_ref("somconnexio.res_partner_2_demo")
        self.partner_sponsored = self.browse_ref(
            "cooperator_somconnexio.res_sponsored_partner_1_demo"
        )

        self.url = "/api/partner"
        self.sponsees_url = self.url + "/sponsees"
        self.check_sponsor_url = self.url + "/check_sponsor"

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.set_up_cooperator_test_data()

    def test_route_get(self):
        partner = self.env.ref('somconnexio.res_partner_2_demo')
        self.assertTrue(partner.member)
        response = self.http_get("{}?vat={}".format(self.url, self.partner.vat))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.reason, "OK")

        content = json.loads(response.content.decode("utf-8"))
        self.assertEqual(
            content["cooperator_register_number"],
            self.partner.cooperator_register_number,
        )
        self.assertEqual(content["cooperator_end_date"], "")
        self.assertEqual(content["sponsorship_code"], self.partner.sponsorship_hash)
        self.assertEqual(content["sponsees_number"], 0)
        self.assertEqual(
            content["sponsees_max"], self.partner.company_id.max_sponsees_number
        )
        self.assertEqual(content["sponsor_ref"], "")
        self.assertEqual(
            content["cooperator_register_number"],
            self.partner.cooperator_register_number,
        )
        self.assertEqual(content["cooperator_end_date"], "")
        self.assertFalse(content["coop_candidate"])
        self.assertTrue(content["member"])

    def test_sponsees_route_get_without_sponsees(self):
        partner = self.browse_ref("somconnexio.res_partner_2_demo")
        self.assertFalse(partner.sponsee_ids)
        content = ResPartnerProcess(self.env).get_partner_sponsorship_data(partner.ref)

        self.assertEqual(content["sponsorship_code"], partner.sponsorship_hash)
        self.assertEqual(content["sponsees_number"], 0)
        self.assertEqual(
            content["sponsees_max"], partner.company_id.max_sponsees_number
        )
        self.assertFalse(content["sponsees"])

    def test_sponsees_route_get_with_SR_as_sponsor(self):
        partner = self.env.ref('somconnexio.res_partner_1_demo')
        SR_sponsee = self.browse_ref(
            "cooperator_somconnexio.sc_subscription_request_2_demo"
        )
        self.assertEqual(SR_sponsee.sponsor_id, partner)
        self.assertTrue(partner.sponsee_ids.inactive_partner)

        content = ResPartnerProcess(self.env).get_partner_sponsorship_data(partner.ref)

        self.assertFalse(content["sponsorship_code"])
        self.assertEqual(content["sponsees_number"], 1)
        self.assertEqual(
            content["sponsees_max"], partner.company_id.max_sponsees_number
        )
        self.assertEqual(content["sponsees"], [SR_sponsee.name])

    def test_sponsees_route_get_with_active_provisioning(self):
        partner = self.partner_sponsored
        self.assertTrue(partner.inactive_partner)
        self.assertFalse(partner.has_lead_in_provisioning)

        # Remove sponsor from a SR
        SR_sponsee = self.browse_ref(
            "cooperator_somconnexio.sc_subscription_request_2_demo"
        )
        self.assertEqual(SR_sponsee.sponsor_id, partner.sponsor_id)
        sponsor = self.env.ref("somconnexio.res_partner_2_demo")
        sponsor.company_id = self.env['res.company'].browse(1)
        SR_sponsee.write({"sponsor_id": sponsor.id})
        self.assertNotEqual(SR_sponsee.sponsor_id, partner.sponsor_id)

        # Create fiber provisioning from same partner
        crm_lead_create(self.env, partner, "fiber")

        self.assertTrue(partner.has_lead_in_provisioning)

        content = ResPartnerProcess(self.env).get_partner_sponsorship_data(
            partner.sponsor_id.ref
        )

        self.assertFalse(content["sponsorship_code"])
        self.assertEqual(content["sponsees_number"], 1)
        self.assertIn(partner.name, content["sponsees"])

    def test_route_sponsees_get_with_active_sponsees(self):
        partner = self.partner_sponsored
        sponsor = partner.sponsor_id

        self.assertTrue(partner.inactive_partner)

        # assign contract to partner
        contract = self.env.ref("somconnexio.contract_fibra_600")
        contract.write(
            {
                "partner_id": partner.id,
                "invoice_partner_id": partner.id,
                "service_partner_id": partner.id,
                "email_ids": [(6, 0, [partner.id])],
            }
        )

        self.assertFalse(partner.inactive_partner)

        res_partner_process = ResPartnerProcess(self.env)
        content = res_partner_process.get_partner_sponsorship_data(sponsor.ref)

        self.assertEqual(content["sponsees_number"], 2)
        self.assertEqual(len(content["sponsees"]), 2)
        self.assertIn(partner.name, content["sponsees"])

    def test_can_sponsor_ok(self):
        self.partner.company_id = self.env['res.company'].browse(1)
        content = ResPartnerProcess(self.env).check_sponsor(
            self.partner.sponsorship_hash,
            self.partner.vat
        )

        self.assertEqual(content["result"], "allowed")
        self.assertEqual(content["message"], "ok")

    def test_can_sponsor_ok_code_insensitive(self):
        self.partner.company_id = self.env['res.company'].browse(1)
        content = ResPartnerProcess(self.env).check_sponsor(
            self.partner.sponsorship_hash.upper(),
            self.partner.vat
        )

        self.assertEqual(content["result"], "allowed")
        self.assertEqual(content["message"], "ok")

    def test_can_sponsor_ko_code_incomplete(self):
        self.Partner = self.env["res.partner"]
        self.subscription_request_1.iban = 'ES91 2100 0418 4502 0005 1332'
        self.subscription_request_1.vat = 'ES71127582J'
        self.subscription_request_1.country_id = self.ref('base.es')
        self.subscription_request_1.validate_subscription_request()
        self.pay_invoice(self.subscription_request_1.capital_release_request)

        content = ResPartnerProcess(self.env).check_sponsor(
            vat=self.subscription_request_1.partner_id.vat,
            sponsor_code=self.subscription_request_1.partner_id.sponsorship_hash[:-1],
        )

        self.assertEqual(content["result"], "not_allowed")
        self.assertEqual(content["message"], "invalid code or vat number")

    def test_can_sponsor_ko_maximum_exceeded(self):
        self.partner.company_id = self.env['res.company'].browse(1)
        self.assertTrue(self.partner.company_id.max_sponsees_number)
        while (
            self.partner.active_sponsees_number
            < self.partner.company_id.max_sponsees_number
        ):
            sr_vals = subscription_request_create_data(self)
            sr_vals.update({"sponsor_id": self.partner.id})
            self.assertTrue(self.env["subscription.request"].create(sr_vals))

        content = ResPartnerProcess(self.env).check_sponsor(
            vat=self.partner.vat,
            sponsor_code=self.partner.sponsorship_hash,
        )

        self.assertEqual(content["result"], "not_allowed")
        self.assertEqual(content["message"], "maximum number of sponsees exceeded")

    def test_can_sponsor_ko_invalid_code_or_vat(self):
        content = ResPartnerProcess(self.env).check_sponsor(
            vat="WRONG VAT",
            sponsor_code="WRONG SPONSOR CODE",
        )

        self.assertEqual(content["result"], "not_allowed")
        self.assertEqual(content["message"], "invalid code or vat number")

    def test_route_get_inactive_partner(self):
        partner = self.partner_sponsored
        res_partner_process = ResPartnerProcess(self.env)
        content = res_partner_process.to_dict(
            res_partner_process.get_partner_by_ref(partner.ref)
        )

        self.assertEqual(content["sponsor_ref"], partner.sponsor_id.ref)

        # assign contract to partner
        contract = self.env.ref("somconnexio.contract_fibra_600")
        contract.write(
            {
                "partner_id": partner.id,
                "invoice_partner_id": partner.id,
                "service_partner_id": partner.id,
                "email_ids": [(6, 0, [partner.id])],
            }
        )

        partner = res_partner_process.get_partner_by_ref(partner.ref)

        self.assertFalse(partner.inactive_partner)
