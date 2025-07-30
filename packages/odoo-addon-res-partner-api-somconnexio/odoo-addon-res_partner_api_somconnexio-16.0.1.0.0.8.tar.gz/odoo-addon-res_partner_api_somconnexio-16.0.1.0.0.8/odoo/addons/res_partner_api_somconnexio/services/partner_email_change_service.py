from odoo.addons.component.core import Component
from odoo.http import request


class ResPartnerEmailChangeService(Component):
    _inherit = "base.rest.service"
    _name = "res.partner.email.change.service"
    _usage = "partner-email-change"
    _collection = "sc.public.services"
    _description = """
        ResPartnerEmailChange service to expose the partners email
         change wizard via API.
    """

    # pylint: disable=locally-disabled, method-required-super
    def create(self, **kwargs):
        self.env["partner.email.change.process"].with_delay().run_from_api(
            **request.params
        )
        return request.make_json_response({"result": "OK"})
