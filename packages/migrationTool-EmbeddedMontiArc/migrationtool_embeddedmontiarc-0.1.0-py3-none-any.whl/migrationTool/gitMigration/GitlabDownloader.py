import datetime
import logging
import os
import subprocess

import git
import gitlab
import typer
from git import RemoteProgress
from rich import print
from rich.console import Console
from rich.progress import track
from rich.table import Table
from tqdm import tqdm

from migrationTool.gitMigration.Downloader import Downloader
from migrationTool.gitMigration.Git import Git
from migrationTool.gitMigration.mavenSecrets import find_env_vars_in_repo
from migrationTool.migration_types import Architecture, Config, Repo

logger = logging.getLogger(__name__)


class GitlabDownloader(Git, Downloader):
  def __init__(self, config: Config):
    super().__init__()
    Downloader.__init__(self, config)
    self.gl = gitlab.Gitlab(url=config.url, private_token=self.config.sourceToken)
    self.gl.auth()

  def scan(self, path: str = "architecture.yaml", verbose: bool = False):
    """
    Scans all repositories and create a yaml file with the architecture of the repositories.
    """
    print("[bold]Scanning Repositories...")
    architecture = Architecture(path)
    for repoID in track(self.config.repoIDS, description="Scan"):
      repo = self.getRepo(repoID)

      repo_name = repo.name
      repo_namespace = self.getNamespace(repo)
      repo_all_branches = self.getBranches(repo)
      repo_active_branches = []
      repo_stale_branches = self.getStaleBranches(repo)
      repo_path = os.path.join(os.getcwd(), "repos", repo_name)

      repo_secrets = {}
      # Get env variables used by maven. Should be recreated in the new repo
      env_variables = find_env_vars_in_repo(repo_path)
      repo_secrets["GITLABTOKEN"] = {"Value": self.config.sourceToken, "Secret": "Y", }
      repo_secrets["CI_API_V4_URL"] = {"Value": self.gl.api_url, "Secret": "N"}
      if env_variables:
        for secret in env_variables:
          if (secret == "CI_JOB_TOKEN" or secret == "CI_API_V4_URL" or secret == "CI_PROJECT_ID"):
            continue
          else:
            repo_secrets[secret] = {"Value": "Please add a value",
                                    "Secret": "Y, if it should be saved as a secret. E, if it already exists. The "
                                              "value should then be the "
                                              "name of the according secret. Default is N", }
      for b in repo_all_branches:
        if b not in repo_stale_branches:
          repo_active_branches.append(b)

      repo_docker_images = self.getDockerImages(repo)
      repo_obj = Repo(repo_name, repoID, repo_docker_images, repo_path, repo_namespace, repo_active_branches,
                      repo_stale_branches, repo_secrets, )
      architecture.add_repo(repo_obj)

    console = Console()
    table = Table("Name", "Status")
    for repoID in self.config.repoIDS:
      repo = architecture.get_repo_by_ID(repoID)
      table.add_row(repo.name, ":white_check_mark:")
    print()
    console.print(table)
    architecture.dump_yaml(verbose)

  def clone(self):
    """
    Clone repositories from GitLab to the local machine.
    """
    logger.info("Cloning Repositories...")
    print("[bold]Cloning Repositories...")
    console = Console()
    table = Table("Repository", "Status")
    for repoID in self.config.repoIDS:
      typer.echo("--------------------------------")
      repo_name, status = self.clone_repo(repoID, os.path.join(os.getcwd(), "repos"))
      table.add_row(repo_name, status)
    print()
    console.print(table)

  def getRepo(self, repoID: str):
    """
    Get the repository object from GitLab by its id.
    :param repoID: GitLab repository ID
    :return: Repository object
    """
    repo = self.gl.projects.get(repoID)
    return repo

  def getBranches(self, repo):
    """
    Get all branches from the repository.
    :param repo: GitLab Repo object
    :return: list - List of branches
    """
    data = []
    branches = repo.branches.list(all=True)
    for branch in branches:
      data.append(branch.name)
    return data

  def getStaleBranches(self, repo):
    """
    Get all branches that are older than 90 days.
    :param repo: GitLab  Repo object
    :return: list - List of stale branches
    """
    cutoff_date = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=90)
    stale_branches = []
    branches = repo.branches.list(all=True)
    for branch in branches:
      commit_date = datetime.datetime.fromisoformat(branch.commit["committed_date"]).replace(
        tzinfo=datetime.timezone.utc)
      if commit_date < cutoff_date:
        stale_branches.append(branch.name)
    return stale_branches

  def getDockerImages(self, repo):
    """
    Get all docker images from the repository.
    :param repo: GitLab Repo object
    :return: list - List of docker images
    """
    data = []
    try:
      images = repo.repositories.list(all=True)
      for image in images:
        try:
          tags = image.tags.list(all=True)
          for tag in tags:
            data.append(image.name + ":" + tag.name)
        except gitlab.exceptions.GitlabListError:
          pass
    except gitlab.exceptions.GitlabListError:
      pass
    return data

  def getMavenArtifacts(self, repo):
    """
    Get all maven artifacts from the repository.
    :param repo: GitLab Repo object
    :return: list - List of maven artifacts
    """
    data = []
    try:
      artifacts = repo.packages.list(all=True)
      for artifact in artifacts:
        data.append(artifact.name)
    except gitlab.exceptions.GitlabListError:
      pass
    return data

  def getNamespace(self, repo):
    """
    Get the namespace of the repository.
    :param repo: GitLab Repo object
    :return: Str - Namespace of the repository
    """
    return repo.namespace["full_path"]

  def clone_repo(self, repo_id, clone_path) -> tuple[str, str]:
    """
    Clone a repository from GitLab to the local machine. Additionally it checks out all branches and removes the
    remote origin.
    :param repo_id: Repository ID in GitLab
    :param clone_path: Path to clone the repository to
    """
    gitlab_repo = self.getRepo(repo_id)
    clone_path = os.path.join(clone_path, gitlab_repo.name)
    # Create authorized URL with private token for cloning
    repo_url = gitlab_repo.http_url_to_repo.replace("https://", f"https://oauth2:{self.config.sourceToken}@")
    logging.info(f"Cloning {gitlab_repo.name} to {clone_path}")
    print(f"Cloning {gitlab_repo.name} to {clone_path}")
    # If a folder with the repos name already exists, skip cloning
    if not os.path.exists(clone_path):
      os.makedirs(clone_path)
    else:
      logging.info(f"Directory {clone_path} already exists, skipping clone.")
      print(f"Directory {clone_path} already exists, skipping clone.")
      return (gitlab_repo.name, ":white_check_mark: [green] Skipped cloning [/green]",)
    # Clone
    default_branch = gitlab_repo.default_branch
    with CloneProgress() as progress:
      git.Repo.clone_from(repo_url, clone_path, branch=default_branch, progress=progress)

    logging.info(f"Cloning {gitlab_repo.name} finished")
    print(f"[green]Cloning {gitlab_repo.name} finished [/green]")

    # Check if LFS is used and download LFS objects if necessary
    lfs_check = subprocess.run(["git", "lfs", "ls-files"], cwd=clone_path, capture_output=True, text=True)
    if lfs_check.stdout:
      logging.info("LFS-Objekte gefunden, LFS-Objekte werden heruntergeladen...")
      typer.echo("LFS-Objekte werden heruntergeladen...")
      process = subprocess.Popen(["git", "lfs", "pull"], cwd=clone_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                 text=True, )
      # for line in process.stdout:
      #    print(line.strip())
      rc = process.poll()

    try:
      local_repo = git.Repo(clone_path)
    except git.exc.InvalidGitRepositoryError:
      logger.error(f"Invalid Git repository at {clone_path}. Please consider deleting the folder manually.")
      typer.echo(f"Invalid Git repository at {clone_path}. Please consider deleting the folder manually.")
      return (gitlab_repo.name, ":x: [red] Invalid Git repository, please delete the folder [/red]",)
    self.checkout_branches(local_repo)
    self.remove_remote_origin(local_repo)
    return (gitlab_repo.name, ":white_check_mark: [green] Successfully cloned [/green]",)

  def checkout_branches(self, repo):
    """
    Checkout all branches available in the remote repository.
    :param repo: repository objec
    """
    console = Console()
    table = Table("Branch", "Status")
    repo.remotes.origin.fetch()  # Fetch all branches from the remote
    for branch in tqdm(repo.remotes.origin.refs, desc="Checking out all branches"):  # Iterate over all remote branches
      branch_name = branch.name.split("/")[-1]  # Extract branch name
      if branch_name == "HEAD":
        continue
      try:
        repo.git.checkout("-B", branch_name, branch.name)  # Create and checkout local branch tracking the remote
        logging.info(f"Checked out branch {branch_name}.")
        table.add_row(branch_name, ":white_check_mark: [green] Successfully checked out [/green]", )
      except Exception as e:
        logging.warning(f"Error checking out branch {branch_name}: {e}")
        table.add_row(branch_name, ":x: [red] Error checking out branch [/red]")

      if "master" in repo.branches:
        repo.git.checkout("master")  # Checkout the master branch
      elif "main" in repo.branches:
        repo.git.checkout("main")  # Checkout the main branch


class CloneProgress(RemoteProgress):
  def __init__(self):
    super().__init__()
    self.pbar = tqdm(desc="Cloning", unit="objects")

  def update(self, op_code, cur_count, max_count=None, message=""):
    self.pbar.total = max_count
    self.pbar.n = cur_count
    self.pbar.refresh()

  def close(self):
    self.pbar.close()

  def __enter__(self):
    return self

  def __exit__(self, exc_type, exc_value, traceback):
    self.close()

  def new_message_handler(self):
    """
    Can be used to print the output of the git push command directly for debugging. To do so remove the __disabled
    from the name
    :return:
        A progress handler suitable for handle_process_output(), passing lines on to this Progress
        handler in a suitable format"""

    def handler(line):
      logger.info(line.rstrip())
      return self._parse_progress_line(line.rstrip())

    return handler


if __name__ == "__main__":
  dr = GitlabDownloader(Config("../../config.yaml"))
  dr.clone()
  dr.scan()
