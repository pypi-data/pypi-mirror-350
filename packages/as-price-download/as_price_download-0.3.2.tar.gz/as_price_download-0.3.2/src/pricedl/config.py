'''
Configuration for the PriceDb application.
'''
import os

from loguru import logger
import tomllib
from pathlib import Path
from typing import Dict, Any, Optional


class PriceDbConfig:
    '''Configuration for the PriceDb application.'''

    def __init__(self):
        self.config_path = self._get_config_path()
        self.config_data = self._load_config()

    def _get_config_path(self) -> Path:
        '''Get the path to the configuration file.'''
        config_dir = None

        # Check for XDG_CONFIG_HOME environment variable
        xdg_config = os.environ.get("XDG_CONFIG_HOME")
        if xdg_config:
            config_dir = Path(xdg_config) / "pricedl"
        else:
            # Default to platform-specific config directory
            home = Path.home()
            if os.name == "posix":  # Linux/Mac
                config_dir = home / ".config" / "pricedb"
            elif os.name == "nt":  # Windows
                appdata = os.environ.get("APPDATA")
                if not appdata:
                    raise RuntimeError("APPDATA environment variable not set")
                # config_dir = home / "AppData" / "Roaming" / "pricedl" / "config"
                config_dir = Path(appdata) / "pricedl" / "config"

        if not config_dir:
            raise RuntimeError("Could not determine configuration directory")

        config_dir.mkdir(parents=True, exist_ok=True)

        # Use the current directory.
        # config_dir = Path.cwd()
        return config_dir / "pricedl.toml"

    def _load_config(self) -> Dict[str, Any]:
        '''Load configuration from file.'''
        if not self.config_path.exists():
            logger.warning(f"Config file not found: {self.config_path}")
            return {}

        with open(self.config_path, "rb") as f:
            return tomllib.load(f) or {}

    # def save_config(self):
    #     '''Save configuration to file.'''
    #     with open(self.config_path, "w") as f:
    #         yaml.dump(self.config_data, f)

    @property
    def prices_path(self) -> Optional[str]:
        '''Path to the prices file.'''
        return self.config_data.get("prices_path")

    # @prices_path.setter
    # def prices_path(self, value: str):
    #     self.config_data["prices_path"] = value
    #     self.save_config()

    @property
    def symbols_path(self) -> Optional[str]:
        '''Path to the symbols file.'''
        return self.config_data.get("symbols_path")


    def get_value(self, key: str) -> Any:
        '''Get a value from the configuration.'''
        return self.config_data.get(key)

    # def set_value(self, key: str, value: Any):
    #     self.config_data[key] = value
    #     self.save_config()
