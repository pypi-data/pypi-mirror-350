from odoo.addons.base_rest.controllers.main import RestController


class APIKeyController(RestController):
    _root_path = "/api/"
    _collection_name = "sc.api.key.services"
    _default_auth = "api_key"


class PublicController(RestController):
    _root_path = "/public-api/"
    _collection_name = "sc.public.services"
    _default_auth = "public"
