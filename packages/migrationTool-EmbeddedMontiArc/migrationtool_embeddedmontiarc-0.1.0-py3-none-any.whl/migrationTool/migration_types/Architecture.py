import logging
import os
import sys
import yaml
from rich import print

from migrationTool.migration_types.Repo import Repo

logger = logging.getLogger(__name__)


class Architecture:
  def __init__(self, filepath: str, repos: dict[str, Repo] = None):
    if repos is None:
      repos = {}
    self.filepath = filepath
    self.repos = repos
    self.repoIDs = repos.keys()

  def add_repo(self, repo: Repo):
    """
    Adds a repo to the architecture
    :param repo: Repo object
    """
    self.repos[repo.ID] = repo

  def dump_yaml(self, verbose: bool = False):
    """
    Dumps the architecture to a yaml file
    :return: None
    """
    data = {}
    if os.path.exists(self.filepath):
      try:
        existing_architecture = Architecture.load_architecture(self.filepath)
      except AttributeError:
        existing_architecture = None
      if existing_architecture is not None:
        for repoID in self.repos:
          if repoID not in existing_architecture.repos:
            data = data | self.repos[repoID].as_yaml()
      else:
        for repoID in self.repos:
          data = data | self.repos[repoID].as_yaml()
    else:
      for repoID in self.repos:
        data = data | self.repos[repoID].as_yaml()
    if data:
      with open(self.filepath, "a") as file:
        yaml.dump(data, file)

    if verbose:
      print(data)

  @staticmethod
  def load_architecture(filepath):
    assert os.path.exists(filepath)
    with open(filepath, "r") as file:
      try:
        architecture = yaml.safe_load(file)
      except yaml.YAMLError as e:
        logger.error(f"Error loading YAML file: {e}")
        print(f"[red]ERROR: Incorrect yml file at {filepath}")
        sys.exit(1)
        return None
      repos = {}
      for repoName in architecture.keys():
        id, repo = Repo.read_from_Architecture(repoName, architecture[repoName])
        repos[id] = repo
    return Architecture(filepath, repos)

  def get_repo_by_ID(self, repoID: str):
    """
    Returns the repo object for the given repoID
    :param repoID: ID of the repo
    :return: Repo object
    """
    if repoID in self.repos:
      return self.repos[repoID]
    else:
      logger.error(f"Repo with ID {repoID} not found.")
      return None

  def get_repo_by_name(self, name: str):
    """
    Returns the repo object for the given name
    :param name: Name of the repo
    :return: Repo object
    """
    for repo in self.repos.values():
      if repo.name == name:
        return repo
    logger.error(f"Repo with name {name} not found.")
    return None

  def get_docker_images(self):
    """
    Returns a list of all docker images in the architecture
    :return: List of docker images
    """
    docker_images = {}
    for repoID, repo in self.repos:
      if repo.docker_images is not None:
        docker_images[repoID] = repo.docker_images
    return docker_images
