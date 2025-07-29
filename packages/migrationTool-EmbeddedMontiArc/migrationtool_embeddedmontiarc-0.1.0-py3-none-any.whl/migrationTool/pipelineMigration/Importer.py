from abc import ABC, abstractmethod

from migrationTool.pipelineMigration.Pipeline import Pipeline


class Importer(ABC):
  """
  Abstract base class for Pipeline importers.
  """

  @abstractmethod
  def getPipeline(self, file: str) -> Pipeline:
    """
    Import a pipeline from a file and return it as a Pipeline object.
    :param file: The file path to the pipeline.
    :type file: str
    :rtype: Pipeline
    :return: An instance of the Pipeline class.
    """
    pass
