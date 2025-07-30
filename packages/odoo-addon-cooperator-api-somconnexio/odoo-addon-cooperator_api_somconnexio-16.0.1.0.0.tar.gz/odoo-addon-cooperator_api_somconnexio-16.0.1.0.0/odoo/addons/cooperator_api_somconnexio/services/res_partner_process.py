from odoo import _
from odoo.fields import Date
from odoo.exceptions import MissingError
from stdnum.util import clean
import logging
_logger = logging.getLogger(__name__)


class ResPartnerProcess:
    def __init__(self, env):
        self.env = env

    def get_partner_by_ref(self, ref):
        domain = [
            ("parent_id", "=", None),
            ("ref", "=", ref),
        ]

        _logger.info("search with domain {}".format(domain))
        partner = self.env["res.partner"].search(domain, limit=1)

        if not partner:
            raise MissingError(_("Partner with ref {} not found.".format(ref)))

        return partner

    def check_sponsor(self, sponsor_code, vat, **kw):
        domain = [
            ("sponsorship_hash", "=", sponsor_code.upper()),
            ("vat", "ilike", self._normalize_vat(vat)),
        ]
        partner = self.env["res.partner"].search(domain, limit=1)
        if not partner:
            result = "not_allowed"
            message = "invalid code or vat number"
        elif not partner.can_sponsor():
            result = "not_allowed"
            message = "maximum number of sponsees exceeded"
        else:
            result = "allowed"
            message = "ok"

        response = {"result": result, "message": message}

        return response

    def get_partner_sponsorship_data(self, ref, **kw):
        partner = self.get_partner_by_ref(ref)
        partner.ensure_one()

        response = {
            "sponsorship_code": partner.sponsorship_hash or "",
            "sponsees_max": partner.company_id.max_sponsees_number,
            "sponsees_number": partner.active_sponsees_number,
            "sponsees": partner.active_sponsees,
        }

        return response

    def _normalize_vat(self, vat):
        chars_to_clean = " -."
        return clean(vat, chars_to_clean).upper().strip()

    def to_dict(self, partner):
        partner.ensure_one()
        partner_dict = {
            "sponsor_ref": partner.sponsor_id.ref or "",
            "coop_agreement_code": partner.coop_agreement_id.code or "",
            "sponsorship_code": partner.sponsorship_hash or "",
            "sponsees_number": partner.active_sponsees_number,
            "sponsees_max": partner.company_id.max_sponsees_number,
            "coop_candidate": partner.coop_candidate,
            "member": partner.member,
            "cooperator_register_number": partner.cooperator_register_number,
            "cooperator_end_date": (
                Date.to_string(partner.cooperator_end_date) or ""
            ),
        }
        return partner_dict
