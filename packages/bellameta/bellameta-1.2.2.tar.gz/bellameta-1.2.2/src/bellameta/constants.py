import os

from bellameta.utils import get_config

BELLAMETA_CONFIG_PATH = os.getenv('BELLAMETA_CONFIG_PATH')
DB_PATH = os.getenv('DB_PATH')
config_data = get_config(config_path=BELLAMETA_CONFIG_PATH)
COHORTS = config_data['COHORTS']
TASKS = config_data['TASKS']
LABEL_TABLE_NAME = config_data['LABEL_TABLE_NAME']
DEFAULT_TABLES = ['state', 'cohort', 'patient', 'section', 'tag', 'stain', 'task', 'year']
# each task comes with its own unique label table, so e.g. Task.Subtyping comes with the subtype table which records the class labels
METADATA_TABLES = DEFAULT_TABLES + list(LABEL_TABLE_NAME.values())