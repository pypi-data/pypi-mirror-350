import logging
from odoo.addons.component.core import Component
from odoo.exceptions import MissingError
from odoo import _

from odoo.addons.somconnexio.helpers.address_service import AddressService
from odoo.addons.somconnexio.helpers.vat_normalizer import VATNormalizer
from . import schemas

_logger = logging.getLogger(__name__)


class ResPartnerService(Component):
    _inherit = "base.rest.service"
    _name = "res.partner.service"
    _usage = "partner"
    _collection = "sc.api.key.services"
    _description = """
        ResPartner service to expose the partners and filter by VAT number.
    """

    def get(self, _id):
        ref = str(_id)
        partner = self._get_partner_by_ref(ref)
        result = self._to_dict(partner)
        return result

    def search(self, vat):
        domain = [
            ("parent_id", "=", None),
            ("vat", "ilike", VATNormalizer(vat).normalize()),
        ]

        _logger.info("search with domain {}".format(domain))
        partners = self.env["res.partner"].search(domain, limit=1)

        if not partners:
            raise MissingError(_("Partner with VAT {} not found.".format(vat)))

        return self._to_dict(partners)

    def _get_partner_by_ref(self, ref):
        domain = [
            ("parent_id", "=", None),
            ("ref", "=", ref),
        ]

        _logger.info("search with domain {}".format(domain))
        partner = self.env["res.partner"].search(domain, limit=1)

        if not partner:
            raise MissingError(_("Partner with ref {} not found.".format(ref)))

        return partner

    def _to_dict(self, partner):
        partner.ensure_one()
        return {
            "id": partner.id,
            "name": partner.name,
            "firstname": partner.firstname or "",
            "lastname": partner.lastname or "",
            "display_name": partner.lastname or "",
            "ref": partner.ref or "",
            "lang": partner.lang or "",
            "vat": partner.vat or "",
            "type": partner.type or "",
            "email": partner.email or "",
            "phone": partner.phone or "",
            "mobile": partner.mobile or "",
            "addresses": self._addresses_to_dict(partner),
            "inactive_partner": partner.inactive_partner,
            "banned_actions": [action.code for action in partner.banned_action_tags],
            "is_company": partner.is_company,
        }

    def _addresses_to_dict(self, partner):
        """
        Convert Partner addresses objects in a list of address dicts
        removing the duplicated addresses.
        """
        addresses = partner.child_ids.filtered(
            lambda addr: addr.type in AddressService.ADDRESS_TYPES
        )
        addresses = addresses | partner
        addresses = addresses.mapped(lambda a: AddressService(self.env, a))
        addresses = list(set(addresses))
        return [addr.__dict__ for addr in addresses]

    def _validator_get(self):
        return schemas.S_RES_PARTNER_REQUEST_GET

    def _validator_return_get(self):
        return schemas.S_RES_PARTNER_RETURN_GET

    def _validator_search(self):
        return schemas.S_RES_PARTNER_REQUEST_SEARCH

    def _validator_return_search(self):
        return schemas.S_RES_PARTNER_RETURN_GET
