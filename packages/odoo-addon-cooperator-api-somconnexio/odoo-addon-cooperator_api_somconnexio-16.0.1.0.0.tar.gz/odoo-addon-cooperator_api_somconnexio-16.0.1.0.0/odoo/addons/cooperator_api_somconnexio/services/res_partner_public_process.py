class ResPartnerPublicProcess:
    _description = """
        Run Contract Change Tariff Request Wizard from API
    """

    def __init__(self, env=False):
        self.env = env

    def run_from_api(self):
        domain_members = [
            ("parent_id", "=", False),
            ("is_customer", "=", True),
            "|",
            ("member", "=", True),
            ("coop_candidate", "=", True),
        ]
        members_number = self.env["res.partner"].sudo().search_count(domain_members)

        response = {"members": members_number}

        return response
