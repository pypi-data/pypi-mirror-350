import logging

from odoo.addons.component.core import Component
from odoo.exceptions import MissingError
from odoo import _

from . import schemas

_logger = logging.getLogger(__name__)


class CoopAgreementService(Component):
    _inherit = "base.rest.service"
    _name = "coop.agreement.service"
    _usage = "coop-agreement"
    _collection = "sc.api.key.services"
    _description = """
        CoopAgreement service to expose the coop agreement and filter by code.
    """

    def search(self, code):
        domain = [
            ("code", "=", code),
        ]
        _logger.info("search with domain {}".format(domain))
        coop_agreement = self.env["coop.agreement"].search(domain, limit=1)
        if not coop_agreement:
            raise MissingError(_("Coop Agreement with code {} not found.".format(code)))

        return self._to_dict(coop_agreement)

    def _to_dict(self, coop_agreement):
        coop_agreement.ensure_one()
        return {
            "name": coop_agreement.partner_id.name,
            "code": coop_agreement.code,
            "first_month_promotion": coop_agreement.first_month_promotion,
        }

    def _validator_search(self):
        return schemas.S_SEARCH_COOP_AGREEMENT

    def _validator_return_search(self):
        return schemas.S_RETURN_SEARCH_COOP_AGREEMENT
