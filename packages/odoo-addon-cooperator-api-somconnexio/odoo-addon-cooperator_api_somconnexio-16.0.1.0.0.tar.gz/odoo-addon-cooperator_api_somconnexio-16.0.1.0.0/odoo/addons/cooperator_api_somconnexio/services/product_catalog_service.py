import logging
from odoo.addons.component.core import Component

from . import schemas

_logger = logging.getLogger(__name__)


class ProductCatalog(Component):
    _inherit = "product_catalog.service"

    def _extract_product_info(self, product, pricelist_id):
        product_info = super(ProductCatalog, self)._extract_product_info(
            product, pricelist_id
        )
        product_info["available_for"] = self._get_product_available_for(product)

        return product_info

    def _get_product_available_for(self, product):
        sponsee_coop_agreement = self.env["coop.agreement"].search(
            [("code", "=", "SC")]
        )
        coop_agreements = self.env["coop.agreement"].search([("code", "!=", "SC")])
        sponsee_products = sponsee_coop_agreement.products
        coop_agreement_products = []
        for coop_agreement in coop_agreements:
            coop_agreement_products += coop_agreement.products

        coop_agreement_products = list(set(coop_agreement_products))

        available_for = ["member"]
        if product.product_tmpl_id in coop_agreement_products:
            available_for += ["coop_agreement"]
        if product.product_tmpl_id in sponsee_products:
            available_for += ["sponsored"]

        return available_for

    def _validator_return_search(self):
        return schemas.S_PRODUCT_CATALOG_RETURN_SEARCH_AVAILABLE_FOR
