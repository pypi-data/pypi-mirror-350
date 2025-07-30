from odoo.addons.base_rest import restapi
from odoo.addons.component.core import Component
from odoo.http import request
from .res_partner_public_process import ResPartnerPublicProcess
import logging

_logger = logging.getLogger(__name__)


class RestPartnerPublicService(Component):
    _name = "res.partner.public.service"
    _inherit = "base.rest.service"
    _collection = "sc.public.services"
    _usage = "partner"
    _description = """
        ResPartner service to expose the count of partners without auth required.
    """

    @restapi.method(
        [(["/count"], "GET")],
    )
    def count(self):
        response = ResPartnerPublicProcess(self.env).run_from_api()
        return request.make_json_response(response)
