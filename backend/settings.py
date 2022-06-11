import pathlib
import yaml
import os
import logging.config

# log = logging.getLogger(__name__)
BASE_DIR = pathlib.Path(__file__).parent
default_config_path = BASE_DIR / 'config' / 'config.yaml'


def load_config_from_file(path):
    with open(str(path)) as f:
        config = yaml.safe_load(f)
        return config


config = {}
if os.path.exists(default_config_path):
    config = load_config_from_file(default_config_path)

# log_config = config['logging']
# logging.config.dictConfig(log_config)



logging.info('configured logging')
