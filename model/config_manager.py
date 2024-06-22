import os
import sys
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class ConfigManager:
    def __init__(self, config_file='config.json'):
        self.config_file = self.get_resource_path(config_file)
        self.config = self.load_config()

    @staticmethod
    def get_resource_path(relative_path):
        """ Get the absolute path to the resource, works for both dev and PyInstaller """
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    def load_config(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, "r") as f:
                return json.load(f)
        return {}

    def save_config(self):
        with open(self.config_file, "w") as f:
            json.dump(self.config, f)

    def get(self, key, default=None):
        return self.config.get(key, default)

    def set(self, key, value):
        self.config[key] = value
        self.save_config()
