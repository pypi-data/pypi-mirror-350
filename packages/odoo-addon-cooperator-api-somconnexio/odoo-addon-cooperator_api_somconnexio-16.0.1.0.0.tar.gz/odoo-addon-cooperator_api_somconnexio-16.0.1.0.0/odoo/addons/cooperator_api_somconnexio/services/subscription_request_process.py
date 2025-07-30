import logging
from odoo import _
from odoo.fields import Date
from odoo.addons.base_rest.http import wrapJsonException
from odoo.addons.somconnexio.helpers.vat_normalizer import VATNormalizer
from werkzeug.exceptions import BadRequest

_logger = logging.getLogger(__name__)


class SubscriptionRequestProcess():
    def __init__(self, env):
        self.env = env

    def create(self, **params):
        params = self._prepare_create(params)
        sr = self.env["subscription.request"].create(params)
        return self._to_dict(sr)

    def _prepare_create(self, params):
        address = params["address"]
        country = self._get_country(address["country"])
        state_id = self._get_state(address["state"], country.id)
        nationality_id = self._get_nationality(params["nationality"])
        payment_type = self._get_payment_type(params["payment_type"])
        sr_create_values = {
            "firstname": params.get("firstname"),
            "lastname": params.get("lastname"),
            "email": params["email"],
            "phone": params.get("phone"),
            "address": address["street"],
            "zip_code": address["zip_code"],
            "city": address["city"],
            "country_id": country.id,
            "state_id": state_id,
            "lang": params["lang"],
            "iban": params.get("iban"),
            "vat": VATNormalizer(params["vat"]).convert_spanish_vat(),
            "discovery_channel_id": params["discovery_channel_id"],
            "nationality": nationality_id,
            "payment_type": payment_type,
            "is_company": params.get("is_company"),
            "company_name": params.get("company_name"),
            "company_email": params.get("company_email"),
            "type": params["type"],
            "source": params.get("source", "website"),
        }
        if not params.get("is_company"):
            sr_create_values["birthdate"] = "{} 00:00:00".format(params["birthdate"])
            sr_create_values["gender"] = params["gender"]
        if params["type"] == "new":
            sr_create_values["share_product_id"] = self.env.ref(
                "cooperator_somconnexio.cooperator_share_product"
            ).product_variant_id.id
            sr_create_values["ordered_parts"] = 1
        elif params["type"] == "sponsorship":
            sponsor = self._get_sponsor(
                VATNormalizer(params["sponsor_vat"]).convert_spanish_vat()
            )
            sr_create_values["sponsor_id"] = sponsor.id
        elif params["type"] == "sponsorship_coop_agreement":
            coop_agreement = self._get_coop_agreement(params["coop_agreement"])
            sr_create_values["coop_agreement_id"] = coop_agreement.id
        return sr_create_values

    def _get_country(self, code):
        country = self.env["res.country"].search([("code", "=", code)])
        if country:
            return country
        else:
            raise wrapJsonException(BadRequest(_("No country for isocode %s") % code))

    def _get_state(self, state, country_id):
        state_id = (
            self.env["res.country.state"]
            .search(
                [
                    ("code", "=", state),
                    ("country_id", "=", country_id),
                ]
            )
            .id
        )
        if not state_id:
            raise wrapJsonException(
                BadRequest("State %s not found" % (state)),
                include_description=True,
            )
        return state_id

    def _get_nationality(self, nationality):
        nationality_id = self.env["res.country"].search([("code", "=", nationality)]).id
        if not nationality_id:
            raise wrapJsonException(
                BadRequest("Nationality %s not found" % (nationality)),
                include_description=True,
            )
        return nationality_id

    def _get_payment_type(self, payment_type):
        if payment_type not in [
            pm[0]
            for pm in self.env["subscription.request"]._fields["payment_type"].selection
        ]:
            raise wrapJsonException(
                BadRequest("Payment type %s not valid" % (payment_type)),
                include_description=True,
            )
        return payment_type

    def _get_sponsor(self, sponsor_vat):
        sponsor = self.env["res.partner"].search(
            [
                ("vat", "ilike", sponsor_vat),
                "|",
                ("member", "=", True),
                ("coop_candidate", "=", True),
            ]
        )
        if not sponsor:
            raise wrapJsonException(
                BadRequest("Sponsor VAT number %s not found" % (sponsor_vat)),
                include_description=True,
            )
        return sponsor

    def _get_coop_agreement(self, code):
        coop_agreement = self.env["coop.agreement"].search([("code", "=", code)])
        if not coop_agreement:
            raise wrapJsonException(
                BadRequest("Coop Agreement code %s not found" % (code)),
                include_description=True,
            )
        return coop_agreement

    def _or_none(self, value):
        if value:
            return value
        else:
            return None

    def _to_dict(self, sr):
        sr.ensure_one()

        return {
            "id": sr.id,
            "is_company": sr.is_company,
            "firstname": sr.firstname,
            "lastname": sr.lastname,
            "email": sr.email,
            "state": sr.state,
            "date": Date.to_string(sr.date),
            "ordered_parts": sr.ordered_parts,
            "address": {
                "street": sr.address,
                "zip_code": sr.zip_code,
                "city": sr.city,
                "country": sr.country_id.code,
            },
            "lang": sr.lang,
            "birthdate": self._or_none(Date.to_string(sr.birthdate)),
            "gender": self._or_none(sr.gender),
            "iban": self._or_none(sr.iban),
            "phone": self._or_none(sr.phone),
            "capital_release_request_date": self._or_none(
                Date.to_string(sr.capital_release_request_date)
            ),
            "capital_release_request": [],
            "data_policy_approved": sr.data_policy_approved,
            "internal_rules_approved": sr.internal_rules_approved,
            "financial_risk_approved": sr.financial_risk_approved,
            "generic_rules_approved": sr.generic_rules_approved,
            "skip_iban_control": sr.skip_iban_control,
        }
