import os

from bellameta.utils import get_config

BELLAMETA_CONFIG_PATH = os.getenv('BELLAMETA_CONFIG_PATH')
DB_PATH = os.getenv('DB_PATH')
SPLIT_TABLES = ['split', 'mode']
config_data = get_config(config_path=BELLAMETA_CONFIG_PATH)
MODE = config_data['MODE']
SPLITNAME = config_data['SPLITNAME']