{
    "version": "16.0.1.0.0",
    "name": "Base Rest - SomConnexio",
    "summary": """
    Expose the basic REST and public API controllers used in Som Connexió.
    """,
    "author": """
        Som Connexió SCCL,
        Coopdevs Treball SCCL
    """,
    "category": "Cooperative Management",
    "website": "https://git.coopdevs.org/coopdevs/som-connexio/odoo/odoo-somconnexio",
    "license": "AGPL-3",
    "depends": [
        "base_rest",
        "auth_api_key",
    ],
    "external_dependencies": {},
    "data": [],
    "demo": ["demo/auth_api_key.xml"],
    "application": False,
    "installable": True,
}
