import logging
from abc import ABC

from migrationTool.migration_types import Config, Architecture

logger = logging.getLogger(__name__)


class Uploader(ABC):
  def __init__(self, config: Config, architecture: Architecture):
    self.architecture = architecture
    self.config = config
