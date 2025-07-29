import os

import git
from git import Repo


class Repo:
  def __init__(self, name: str, repoID: str, images: list[str], path: str, namespace: str, active_branches: list[str],
               stale_branches: list[str], secrets: list, secrets_to_create: tuple[str, str] = [], ):
    self.name = name
    self.ID = repoID
    self.images = images
    self.path = path
    self.namespace = namespace
    self.active_branches = active_branches
    self.stale_branches = stale_branches
    self.secrets = secrets
    self.secrets_to_create = secrets_to_create

  def get_repo(self):
    return git.Repo(self.path)

  def __str__(self):
    Output = "---------"
    Output += f"Repo: {self.name}\n"
    Output += f"ID: {self.ID}\n"
    Output += f"Images: {self.images}\n"
    Output += f"Location: {self.path}\n"
    Output += f"Namespace: {self.namespace}\n"
    Output += f"Active branches: {self.active_branches}\n"
    Output += f"Stale branches: {self.stale_branches}\n"
    Output += "---------"
    return Output

  @staticmethod
  def read_from_Architecture(name: str, architecture: dict[str, str | list[str] | dict]) -> tuple[str, Repo]:
    """
    Reads the repo name and id from the architecture file.
    :param repoID: Id of the repository
    :param architecture: Architecture file
    :return: Tuple of repo name and id
    """
    active_branches = architecture.get("Branches", [])
    stale_branches = architecture.get("StaleBranches", [])
    namespace = architecture.get("Namespace", "")
    docker_images = architecture.get("DockerImages", [])
    path = os.path.join(os.getcwd(), "repos", name)
    id = architecture.get("ID", "")
    secrets = []
    secrets_to_create = []
    if "Secrets" in architecture:
      for secret_name, secret in architecture["Secrets"].items():
        if secret["Value"] == "Please add a value":
          continue
        if secret["Secret"].lower() == "y":
          secrets.append(secret_name)
          secrets_to_create.append((secret_name, secret["Value"]))
        elif secret["Secret"].lower() == "e":
          secrets.append((secret_name, "${{ secrets." + str(secret["Value"]) + " }}"))
        else:
          secrets.append((secret_name, secret["Value"]))
    return id, Repo(name, id, docker_images, path, namespace, active_branches, stale_branches, secrets,
                    secrets_to_create, )

  def get_branches_to_be_migrated(self) -> list[str]:
    """
    Returns the branches to be migrated.
    :return: List of branches to be migrated
    """
    if self.active_branches is None:
      return self.stale_branches
    elif self.stale_branches is None:
      return self.active_branches
    else:
      return list(set(self.active_branches).union(set(self.stale_branches)))

  def as_yaml(self) -> dict[str, str | list[str] | dict]:
    """
    Returns the repo as a yaml-dict.
    :return: Yaml-like dict of the repo
    """
    data = {"ID": self.ID, "Namespace": self.namespace, "Path": self.path, "Secrets": self.secrets, }
    if self.active_branches:
      data["Branches"] = self.active_branches
    if self.stale_branches:
      data["StaleBranches"] = self.stale_branches
    if self.images:
      data["DockerImages"] = self.images
    return {self.name: data}
