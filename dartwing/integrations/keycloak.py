"""Placeholder for Keycloak integration."""


class KeycloakClient:
    def __init__(self):
        self.base_url = None

    def configure(self, base_url: str):
        self.base_url = base_url

    def is_configured(self) -> bool:
        return bool(self.base_url)
