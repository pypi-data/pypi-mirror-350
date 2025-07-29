# metaworkflows/metaworkflows/__init__.py
import logging.config
import os
from pathlib import Path
from metaworkflows.core.connections import get_connection_manager
# from metaworkflows.constants import CONNECTIONS_PATH_DEV
# Navigates to project root's config
CONFIG_PATH = Path(__file__).parent.parent / "config"

def setup_logging(default_path=CONFIG_PATH / 'logging.conf', default_level=logging.INFO, env_key='LOG_CFG'):
    """Setup logging configuration"""
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = Path(value)
    if path.exists():
        logging.config.fileConfig(path, disable_existing_loggers=False)
    else:
        logging.basicConfig(
            level=default_level, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        logging.warning(
            f"Logging configuration file not found at {path}. Using basicConfig.")

# def load_connections(file_path=CONFIG_PATH / 'connections.yaml'):
#     """Loads connection configurations."""
#     if not file_path.exists():
#         logging.error(f"Connections configuration file not found: {file_path}")
#         return {}
#     with open(file_path, 'r') as f:
#         # Simple environment variable substitution
#         content = f.read()
#         import re
#         for match in re.finditer(r"\$\{(.*?)\}", content):
#             env_var = match.group(1)
#             value = os.getenv(env_var, "")
#             content = content.replace(f"${{{env_var}}}", value)
#         connections = yaml.safe_load(content)
#     return connections.get('connections', {}) if connections else {}

setup_logging()
# CONNECTIONS = load_connections()
CONNECTION_MANAGER = get_connection_manager(source_type="secret")

# Define a base directory for the project if needed for resolving relative paths in jobs
PROJECT_ROOT = Path(__file__).parent.parent.parent
