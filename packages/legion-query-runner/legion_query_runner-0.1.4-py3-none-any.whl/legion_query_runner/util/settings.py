import os
from typing import Dict, Any

class DynamicSettings:
    def __init__(self):
        self._settings: Dict[str, Any] = {}

    def set(self, key: str, value: Any) -> None:
        self._settings[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        return self._settings.get(key, default)

    def ssh_tunnel_auth(self) -> Dict[str, Any]:
        return {
            "ssh_pkey": self.get("ssh_pkey"),
            "ssh_private_key_password": self.get("ssh_private_key_password"),
        }

dynamic_settings = DynamicSettings()

# Default settings
SCHEMA_RUN_TABLE_SIZE_CALCULATIONS = os.environ.get("SCHEMA_RUN_TABLE_SIZE_CALCULATIONS", "false").lower() == "true"
BIGQUERY_HTTP_TIMEOUT = int(os.environ.get("BIGQUERY_HTTP_TIMEOUT", "600")) 