from odoo.addons.base_rest_somconnexio.services.validator_helper import date_validator
from odoo.addons.somconnexio.services.schemas import (
    S_ADDRESS_CREATE,
    S_PRODUCT_CATALOG_RETURN_SEARCH,
)

S_PARTNER_CHECK_CAN_SPONSOR = {
    "sponsor_code": {"type": "string", "required": True},
    "vat": {"type": "string", "required": True},
}
S_PARTNER_GET_SPONSEES = {
    "ref": {"type": "string", "required": True},
}

S_DISCOVERY_CHANNEL_REQUEST_SEARCH = {"_id": {"type": "integer"}}

S_DISCOVERY_CHANNEL_RETURN_SEARCH = {
    "discovery_channels": {
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {
                "id": {"type": "integer", "required": True},
                "name": {"type": "string", "required": True},
            },
        },
    }
}

S_SEARCH_COOP_AGREEMENT = {
    "code": {
        "type": "string",
        "required": True,
    }
}

S_RETURN_SEARCH_COOP_AGREEMENT = {
    "name": {
        "type": "string",
        "required": True,
    },
    "code": {
        "type": "string",
        "required": True,
    },
    "first_month_promotion": {
        "type": "boolean",
        "required": True,
    },
}

S_SUBSCRIPTION_REQUEST_RETURN_CREATE = {
    "id": {"type": "integer", "required": True},
    "email": {"type": "string", "required": True, "empty": False},
    "is_company": {"type": "boolean", "required": True},
    "firstname": {"empty": True},
    "lastname": {"empty": True},
    "date": {"type": "string", "required": True, "empty": False},
    "state": {"type": "string", "required": True, "empty": False},
    "ordered_parts": {"type": "integer", "required": True},
    "share_product": {
        "type": "dict",
        "schema": {
            "id": {"type": "integer", "required": True},
            "name": {"type": "string", "required": True, "empty": False},
        },
    },
    "phone": {"type": "string", "required": True, "empty": False, "nullable": True},
    "iban": {"type": "string", "required": True, "empty": False, "nullable": True},
    "address": {
        "type": "dict",
        "schema": {
            "street": {"type": "string", "required": True, "empty": False},
            "zip_code": {"type": "string", "required": True, "empty": False},
            "city": {"type": "string", "required": True, "empty": False},
            "country": {"type": "string", "required": True, "empty": False},
        },
    },
    "lang": {"type": "string", "required": True, "empty": False},
    "capital_release_request": {
        "type": "list",
        "schema": {"type": "integer"},
        "required": True,
        "empty": True,
    },
    "gender": {"type": "string", "required": True, "empty": False, "nullable": True},
    "birthdate": {"type": "string", "check_with": date_validator, "nullable": True},
    "capital_release_request_date": {
        "type": "string",
        "check_with": date_validator,
        "nullable": True,
    },
    "generic_rules_approved": {"type": "boolean", "required": True},
    "skip_iban_control": {"type": "boolean", "required": True},
    "data_policy_approved": {"type": "boolean", "required": True},
    "internal_rules_approved": {"type": "boolean", "required": True},
    "financial_risk_approved": {"type": "boolean", "required": True},
}

S_SUBSCRIPTION_REQUEST_CREATE = {
    "firstname": {"type": "string", "required": True, "empty": False},
    "lastname": {"type": "string", "required": True, "empty": False},
    "is_company": {"type": "boolean", "required": True},
    "email": {"type": "string", "required": True, "empty": False},
    "company_email": {"type": "string"},
    "ordered_parts": {"type": "integer", "required": True},
    "share_product": {"type": "integer", "required": True},
    "address": {
        "type": "dict",
        "schema": {
            "street": {"type": "string", "required": True, "empty": False},
            "zip_code": {"type": "string", "required": True, "empty": False},
            "city": {"type": "string", "required": True, "empty": False},
            "country": {"type": "string", "required": True, "empty": False},
        },
    },
    "lang": {"type": "string", "required": True, "empty": False},
    "phone": {"type": "string", "nullable": True},
    "iban": {"type": "string", "nullable": True},
    "gender": {"type": "string", "nullable": True},
    "birthdate": {"type": "string", "check_with": date_validator, "nullable": True},
    "capital_release_request_date": {
        "type": "string",
        "check_with": date_validator,
        "nullable": True,
    },
    "data_policy_approved": {"type": "boolean"},
    "internal_rules_approved": {"type": "boolean"},
    "financial_risk_approved": {"type": "boolean"},
    "generic_rules_approved": {"type": "boolean"},
    "skip_iban_control": {"type": "boolean"},
}


S_SUBSCRIPTION_REQUEST_CREATE_SC_FIELDS = {
    "iban": {"type": "string"},
    "vat": {"type": "string", "required": True},
    "coop_agreement": {"type": "string"},
    "sponsor_vat": {"type": "string"},
    "voluntary_contribution": {"type": "float"},
    "nationality": {"type": "string"},
    "payment_type": {"type": "string", "required": True},
    "address": {"type": "dict", "schema": S_ADDRESS_CREATE},
    "type": {"type": "string", "required": True},
    "share_product": {"type": "integer", "required": False},
    "ordered_parts": {"type": "integer", "required": False},
    "discovery_channel_id": {"type": "integer", "required": True},
    "birthdate": {"type": "string", "regex": "\\d{4}-[01]\\d-[0-3]\\d"},
    "gender": {"type": "string"},
    "phone": {"type": "string"},
    "is_company": {"type": "boolean"},
    "company_name": {"type": "string"},
    "firstname": {"type": "string"},
    "lastname": {"type": "string"},
    "source": {
        "type": "string",
        "allowed": ["website", "crm", "manual", "operation", "website_change_owner"],
    },
}

S_SUBSCRIPTION_REQUEST_RETURN_CREATE_SC_FIELDS = {
    "share_product": {"required": False},
    "ordered_parts": {"type": "integer", "required": False},
}

S_RES_PARTNER_RETURN_GET = {
    "cooperator_register_number": {"type": "integer"},
    "cooperator_end_date": {"type": "string"},
    "coop_agreement_code": {"type": "string"},
    "sponsorship_code": {"type": "string"},
    "sponsor_ref": {"type": "string"},
    "sponsees_number": {"type": "integer"},
    "sponsees_max": {"type": "integer"},
    "coop_candidate": {"type": "boolean"},
    "member": {"type": "boolean"},
}

S_PARTNER_RETURN_COUNT = {
    "members": {
        "type": "integer",
        "required": True,
    },
}


S_PRODUCT_CATALOG_RETURN_SEARCH_AVAILABLE_FOR = {
    **S_PRODUCT_CATALOG_RETURN_SEARCH,
    "pricelists": {
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {
                **S_PRODUCT_CATALOG_RETURN_SEARCH["pricelists"]["schema"]["schema"],
                "products": {
                    "type": "list",
                    "schema": {
                        "type": "dict",
                        "schema": {
                            **S_PRODUCT_CATALOG_RETURN_SEARCH["pricelists"]["schema"][
                                "schema"
                            ]["products"]["schema"]["schema"],
                            "available_for": {
                                "type": "list",
                                "required": True,
                                "schema": {
                                    "type": "string",
                                },
                            },
                        },
                    },
                },
                "packs": {
                    "type": "list",
                    "schema": {
                        "type": "dict",
                        "schema": {
                            **S_PRODUCT_CATALOG_RETURN_SEARCH["pricelists"]["schema"][
                                "schema"
                            ]["packs"]["schema"]["schema"],
                            "available_for": {
                                "type": "list",
                                "required": True,
                                "schema": {
                                    "type": "string",
                                },
                            },
                        },
                    },
                },
            },
        },
    },
}

S_CRM_LEAD_CREATE = {
    "partner_id": {
        "type": "string",
        "empty": False,
        "required": True,
        "excludes": ["subscription_request_id"],
    },
    "subscription_request_id": {
        "type": "integer",
        "empty": False,
        "required": True,
        "excludes": ["partner_id"],
    },
}
