from .subscription_request_process import SubscriptionRequestProcess
from odoo.addons.component.core import Component

from . import schemas


class SubscriptionRequestService(Component):
    _inherit = "base.rest.service"
    _name = "subscription.request.service"
    _usage = "subscription-request"
    _collection = "sc.api.key.services"
    _description = """
        Subscription Request Services
    """

    # pylint: disable=method-required-super
    def create(self, **params):
        return SubscriptionRequestProcess(self.env).create(**params)

    def _validator_create(self):
        create_schema = schemas.S_SUBSCRIPTION_REQUEST_CREATE
        create_schema.update(schemas.S_SUBSCRIPTION_REQUEST_CREATE_SC_FIELDS)
        return create_schema

    def _validator_return_create(self):
        create_schema = schemas.S_SUBSCRIPTION_REQUEST_RETURN_CREATE
        create_schema.update(schemas.S_SUBSCRIPTION_REQUEST_RETURN_CREATE_SC_FIELDS)
        return create_schema
