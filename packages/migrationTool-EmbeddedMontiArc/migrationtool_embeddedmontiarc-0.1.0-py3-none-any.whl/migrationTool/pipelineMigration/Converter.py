import os
import re
import shutil
from abc import ABC, abstractmethod

from migrationTool.pipelineMigration.Pipeline import Pipeline


class Converter(ABC):
  """
  Abstract base class for Pipeline importers.
  """

  @abstractmethod
  def __init__(self, pipeline: Pipeline):
    self.pipeline = pipeline

  @abstractmethod
  def parse_pipeline(self, **kwargs) -> str:
    """
    Parses the pipeline and returns it in the converted form as a string.
    :rtype: str
    :return: Converted pipeline
    """

  @abstractmethod
  def parse_job(self, job, **kwargs) -> str:
    """
    Parses the job and returns it in the converted form as a string.
    :rtype: str
    :return: Converted job
    """

  @staticmethod
  def set_indentation_to_two_spaces(input_string: str) -> str:
    """
    Sets the tab indentation to two spaces.
    :param input_string:
    :return: Output string with two spaces indentation
    """
    return input_string.replace("\t", "  ")

  @staticmethod
  def replace_job_token_in_settings(file_path, backup=False):
    """
    Replaces 'Job-Token' with 'Private-Token' in the file.
    :param file_path: Path to the file
    :param backup: If True, creates a backup of the original file
    """
    with open(file_path, "r", errors="ignore") as file:
      content = file.read()

    if "Job-Token" or "Private-Token" in content:
      if backup:
        backup_path = file_path + ".bak"
        shutil.copy(file_path, backup_path)

      # Replaces 'Job-Token' with 'Private-Token'
      updated_content = content.replace("Job-Token", "Private-Token")
      # Regex pattern to match the <property> block with Private-Token. Used to replace false hardcoded values
      pattern = r"""
            <property>\s*
            <name>Private-Token</name>\s*
            <value>.*?</value>\s*
            </property>
            """

      # Replaces only the <value> of the matched block with the environment variable
      def replace_value(match):
        return re.sub(r"<value>.*?</value>", "<value>${env.GITLABTOKEN}</value>", match.group(0), )

      updated_content = re.sub(pattern, replace_value, updated_content, flags=re.DOTALL | re.VERBOSE)

      with open(file_path, "w") as file:
        file.write(updated_content)

  @staticmethod
  def process_settings_files(repo_path):
    """
    Searches for settings.xml and ci_settings.xml files in the repository and replaces 'Job-Token' with 'Private-Token
    :param repo_path: Path to the repository
    """
    for root, _, files in os.walk(repo_path):
      for file in files:
        if file == "settings.xml" or file == "ci_settings.xml":
          file_path = os.path.join(root, file)
          Converter.replace_job_token_in_settings(file_path)
