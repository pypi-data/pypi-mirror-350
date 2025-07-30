import os
import yaml
from typing import Any, Optional


class ConfigLoader:
    """
    Loads configuration from Kubernetes mounted ConfigMap or fallback .env file.
    Example:
        loader = ConfigLoader("/etc/config/config.yaml")
        db_host = loader.get("DATABASE_HOST", "localhost")
    """

    def __init__(self, config_file: Optional[str] = "/etc/config/config.yaml"):
        self.config = {}
        if config_file and os.path.exists(config_file):
            with open(config_file, "r") as file:
                self.config = yaml.safe_load(file) or {}
        else:
            # Fall back to environment variables
            self.config = dict(os.environ)

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        return self.config.get(key, default)


# Singleton Loader
config_loader = ConfigLoader()
