import logging
from typing import Any, Dict

from metaworkflows.core.connections import BaseConnectionManager
from metaworkflows.engines.base import BaseEngine

logger = logging.getLogger(__name__)


class BashEngine(BaseEngine):
    def __init__(self, engine_config: Dict[str, Any], connections: BaseConnectionManager):
        super().__init__(engine_config, connections)
        self.env = None
        logger.info("BashEngine initialized.")

    def initialize(self):
        logger.warning("BashEngine initialization complete.")

    def execute(self, yaml_file: str, step_name: str):
        # logger.info(
        #     f"Bash run command with options: {options}")
        pass
