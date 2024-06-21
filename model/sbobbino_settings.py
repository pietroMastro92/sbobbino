import logging
import configparser

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class SbobbinoSettings:
    def __init__(self, config_file='sbobbino.ini'):
        self.config_file = config_file
        self.config = configparser.ConfigParser()
        self.config.read(config_file)
        
    def get_property(self, section, option):
        return self.config.get(section, option)