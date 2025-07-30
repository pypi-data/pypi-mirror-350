from odoo.addons.somconnexio.services.schemas import S_ADDRESS_CREATE

S_RES_PARTNER_REQUEST_GET = {"_id": {"type": "integer"}}

S_RES_PARTNER_REQUEST_SEARCH = {
    "vat": {"type": "string", "required": True},
}

S_RES_PARTNER_RETURN_GET = {
    "id": {"type": "integer"},
    "name": {"type": "string"},
    "firstname": {"type": "string"},
    "lastname": {"type": "string"},
    "display_name": {"type": "string"},
    "ref": {"type": "string"},
    "lang": {"type": "string"},
    "vat": {"type": "string"},
    "type": {"type": "string"},
    "email": {"type": "string"},
    "phone": {"type": "string"},
    "mobile": {"type": "string"},
    "birthdate_date": {"type": "string"},
    "addresses": {
        "type": "list",
        "schema": {"type": "dict", "schema": S_ADDRESS_CREATE},
    },
    "banned_actions": {"type": "list", "schema": {"type": "string"}},
    "inactive_partner": {"type": "boolean"},
    "is_company": {"type": "boolean"},
}
S_PARTNER_EMAIL_CHANGE_CREATE = {
    "partner_id": {"type": "string", "required": True},
    "email": {"type": "string", "required": True},
    "start_date": {"type": "string"},
    "summary": {"type": "string"},
    "done": {"type": "boolean"},
}
