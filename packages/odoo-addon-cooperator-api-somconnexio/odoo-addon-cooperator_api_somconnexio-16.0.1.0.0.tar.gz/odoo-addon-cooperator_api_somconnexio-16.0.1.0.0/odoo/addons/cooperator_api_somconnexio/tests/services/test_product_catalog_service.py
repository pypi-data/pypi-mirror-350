import json

from odoo.addons.somconnexio.tests.test_product_catalog_service import (
    TestProductCatalogController as BaseTest,
)


class TestProductCatalogController(BaseTest):
    def test_product_mobile_available_for(self):
        response = self.http_get("{}&categ=mobile".format(self.url_with_code))

        content = json.loads(response.content.decode("utf-8"))
        obtained_pricelists = content.get("pricelists")
        obtained_mobile_catalog = obtained_pricelists[0].get("products")

        self.assertEqual(
            obtained_mobile_catalog[0]["available_for"],
            ["member", "coop_agreement", "sponsored"],
        )

    def test_product_fiber_available_for(self):
        response = self.http_get("{}&categ=fiber".format(self.url_with_code))

        content = json.loads(response.content.decode("utf-8"))
        obtained_pricelists = content.get("pricelists")
        obtained_fiber_catalog = obtained_pricelists[0].get("products")

        self.assertEqual(obtained_fiber_catalog[0]["available_for"], ["member"])
