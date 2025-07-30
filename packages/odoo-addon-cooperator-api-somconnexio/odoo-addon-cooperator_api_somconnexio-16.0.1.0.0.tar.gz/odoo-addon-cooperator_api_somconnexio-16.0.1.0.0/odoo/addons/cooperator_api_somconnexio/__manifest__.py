{
    "version": "16.0.1.0.0",
    "name": "Cooperator API - SomConnexio",
    "summary": """
        Expose a REST API to integrate cooperators and sponsorship to Som Connexió
        partner structure.
    """,
    "author": """
        Som Connexió SCCL,
        Coopdevs Treball SCCL
    """,
    "category": "Cooperative Management",
    "website": "https://git.coopdevs.org/coopdevs/som-connexio/odoo/odoo-somconnexio",
    "license": "AGPL-3",
    "depends": [
        "base_rest_somconnexio",
        "cooperator_somconnexio",
        "crm_lead_api_somconnexio",
        "res_partner_api_somconnexio"
    ],
    "data": [],
    "demo": [],
    "external_dependencies": {
        "python": ["stdnum"],
    },
    "application": False,
    "installable": True,
}
