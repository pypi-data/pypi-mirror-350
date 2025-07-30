from odoo.addons.base_rest import restapi
from odoo.addons.component.core import Component
from odoo.http import serialize_exception as _serialize_exception
from odoo.http import request
from .res_partner_process import ResPartnerProcess
import functools
import werkzeug
import json
from . import schemas

import logging

_logger = logging.getLogger(__name__)


def serialize_exception(f):
    @functools.wraps(f)
    def wrap(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            _logger.exception("An exception occured during an http request")
            se = _serialize_exception(e)
            error = {
                'code': 200,
                'message': "Odoo Server Error",
                'data': se
            }
            return werkzeug.exceptions.InternalServerError(json.dumps(error))
    return wrap


class ResPartnerService(Component):
    _inherit = "res.partner.service"
    _description = """
        Sponsorship relation between partners
    """

    @restapi.method(
        [(["/check_sponsor"], "GET")],
        input_param=restapi.CerberusValidator(schemas.S_PARTNER_CHECK_CAN_SPONSOR),
    )
    @serialize_exception
    def check_sponsor(self, sponsor_code, vat, **kw):
        response = ResPartnerProcess(self.env).check_sponsor(sponsor_code, vat, **kw)
        return request.make_json_response(response)

    @restapi.method(
        [(["/count"], "GET")],
        auth="public",
        output_param=restapi.CerberusValidator(schemas.S_PARTNER_RETURN_COUNT),
    )
    def count(self):
        domain_members = [
            ("parent_id", "=", False),
            ("customer", "=", True),
            "|",
            ("member", "=", True),
            ("coop_candidate", "=", True),
        ]
        members_number = self.env["res.partner"].sudo().search_count(domain_members)

        return {"members": members_number}

    @restapi.method(
        [(["/sponsees"], "GET")],
        input_param=restapi.CerberusValidator(schemas.S_PARTNER_GET_SPONSEES),
    )
    def get_partner_sponsorship_data(self, ref, **kw):
        response = ResPartnerProcess(self.env).get_partner_sponsorship_data(
            ref, **kw
        )

        return request.make_json_response(response)

    def _validator_return_get(self):
        create_schema = super()._validator_return_get()
        create_schema.update(schemas.S_RES_PARTNER_RETURN_GET)
        return create_schema

    def _validator_return_search(self):
        create_schema = super()._validator_return_search()
        create_schema.update(schemas.S_RES_PARTNER_RETURN_GET)
        return create_schema

    def _to_dict(self, partner):
        dictionary = super()._to_dict(partner)
        dictionary.update(ResPartnerProcess(self.env).to_dict(partner))
        return dictionary
