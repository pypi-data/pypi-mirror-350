from werkzeug.exceptions import BadRequest
from odoo.addons.base_rest.http import wrapJsonException
from odoo.addons.component.core import Component
from . import schemas


class CRMLeadService(Component):
    _inherit = "crm.lead.services"

    # pylint: disable=method-required-super
    def create(self, **params):
        params = self._prepare_create(params)
        # tracking_disable=True in context is needed
        # to avoid to send a mail in CRMLead creation
        sr = self.env["crm.lead"].with_context(tracking_disable=True).create(params)
        return self._to_dict(sr)

    def _subscription_request_id(self, sr_id):
        if not sr_id:
            return False
        sr = self.env["subscription.request"].browse(sr_id)

        if not sr.exists():
            raise wrapJsonException(
                BadRequest("SubscriptionRequest with id %s not found" % (sr_id)),
                include_description=True,
            )

        return sr.id

    def _prepare_create(self, params):
        sr_id = params.get("subscription_request_id")
        params = super()._prepare_create(params)

        params["subscription_request_id"] = self._subscription_request_id(sr_id)
        return params

    def _validator_create(self):
        create_schema = super()._validator_create()
        create_schema.update(schemas.S_CRM_LEAD_CREATE)
        return create_schema
