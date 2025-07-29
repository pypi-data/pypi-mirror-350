import logging
import os

import git
from rich import print
from rich.console import Console
from rich.progress import Progress
from rich.table import Table

from migrationTool.migration_types import Architecture, Config
from migrationTool.pipelineMigration.DockerMigration import DockerMigration
from migrationTool.pipelineMigration.GithubConverter import GithubActionConverter
from migrationTool.pipelineMigration.GithubSubtreeConverter import (GithubSubTreeConverter, )
from migrationTool.pipelineMigration.GitlabCIImporter import GitlabCIImporter


def writeStringToFile(file_path, content):
  with open(file_path, "w") as file:
    file.write(content)


logger = logging.getLogger(__name__)


# ToDo: Test
def GitlabToGithub(repoID: str, architecture: Architecture, config: Config, name: str = "") -> None:
  """
  This function migrates a Pipeline from GitLab to GitHub.
  :param repoID: The ID of the repository to be migrated.
  :param architecture: The architecture object
  :param config: The configuration object.
  :param name: The name of the pipeline.
  :param secrets: A list of names for secrets to be used in the pipeline.
  """
  repo = architecture.get_repo_by_ID(repoID)
  # Open the Gitlab CI file and parse it
  file = open(os.path.join(repo.path, "/.gitlab-ci.yml"), "r")
  pipeline = GitlabCIImporter().getPipeline(file)
  file.close()

  # Change the image names in the pipeline to the migrated registry ones if necessary
  pipeline = changeToUpdatedImages(pipeline, architecture, config, repoID)

  # Open the git repository
  repo_git = repo.get_repo()
  # Converts the maven files to be compatible with the private token and commit changes
  GithubActionConverter.process_settings_files(repo.path)
  repo_git.git.add(all=True)
  repo_git.index.commit("Changed maven settings to private token")

  # Convert the pipeline to Github Actions format
  pipelineConverter = GithubActionConverter(pipeline)
  convertedPipeline = pipelineConverter.parse_pipeline(name, repo.secrets)
  file_path = os.path.join(repo.path, f"./.github/workflows/{name}.yml")
  folder_path = os.path.dirname(file_path)
  # Ordner erstellen, falls sie nicht existieren
  if not os.path.exists(folder_path):
    os.makedirs(folder_path)
    print(f"Ordner '{folder_path}' wurde erstellt.")
  writeStringToFile(file_path, convertedPipeline)
  # Commit the new action
  repo.git.add(all=True)
  repo.index.commit("Migrated pipeline from Gitlab to Github")


def changeToUpdatedImages(progress, docker_migration, pipeline):
  """
  Changes the image names in the pipeline to the updated ones.
  :param pipeline: The pipeline object
  :param architecture: The architecture object
  :param repoID: The ID of the repository
  """
  dependencies = set()
  # Change the image names in the pipeline object
  for _, job in pipeline.jobs.items():
    new_dependencie, job.image = docker_migration.get_new_Image(progress, job.image)
    if new_dependencie:
      dependencies.add(new_dependencie)
  return dependencies, pipeline


def GitlabToGithubSubtree(architecture: Architecture, config: Config, rebuild=False):
  """
      Converts Gitlab pipelines to Github Actions pipelines for all repositories in the subtree monorepo and commits
      the changes.
  :param repoIDS: RepoIDS of the contained repos
  :param architecture: Architecture object
  :param config: Config object
  :param secrets: Secrets to be used in the pipeline
  """
  console = Console()
  github_file_path = os.path.join(os.getcwd(), "repos", config.monorepoName)
  subtree_repo = git.Repo(github_file_path)
  file_path_base = os.path.join(github_file_path, ".github", "workflows")

  # Converts the maven files to be compatible with the private token and commit changes
  GithubActionConverter.process_settings_files(github_file_path)
  subtree_repo.git.add(all=True)
  subtree_repo.index.commit(f"Changed maven settings to private token")

  github_repo_prefix = {}  # Path to each subtree in the monorepo
  monorepoNamespace = config.monorepoNamespace.split("/")
  for repoID in config.repoIDS:
    repo = architecture.get_repo_by_ID(repoID)
    repoNamespace = "/".join([i for i in repo.namespace.split("/") if i not in monorepoNamespace])
    github_repo_prefix[repo.name] = os.path.join(repoNamespace, repo.name)

  # Create Github action folder
  if not os.path.exists(file_path_base):
    os.makedirs(file_path_base)
    logger.info(f"Ordner '{file_path_base}' wurde erstellt.")
  print(f"Trying to convert following pipelines in monorepo at {github_file_path}...")

  branches_to_be_migrated = {}
  iterations = 0
  table = Table("Repository name", "Branch")
  for repoID in config.repoIDS:
    repo = architecture.get_repo_by_ID(repoID)
    branches_to_be_migrated[repoID] = repo.get_branches_to_be_migrated()
    for branch in branches_to_be_migrated[repoID]:
      table.add_row(repo.name, branch)
    iterations += len(branches_to_be_migrated[repoID])
  console.print(table)

  summary = {}
  docker_migration = DockerMigration(architecture, config, "docker_images.txt")
  dependencies = set()
  with Progress() as progress:
    task = progress.add_task("Migrating", total=iterations)
    # Migrate all contained repos
    for repoID in config.repoIDS:
      repo = architecture.get_repo_by_ID(repoID)
      summary[repo.name] = {}
      # Check, which branches were migrated for the repo
      multiple = len(branches_to_be_migrated[str(repoID)]) > 1
      # Iterate over all migrated branches
      for branch in branches_to_be_migrated[str(repoID)]:
        # Chose path to gitlab pipeline according to structure
        if multiple:
          path = os.path.join(github_file_path, github_repo_prefix[repo.name], branch)
        else:
          path = os.path.join(github_file_path, github_repo_prefix[repo.name])

        # Import gitlab pipeline
        try:
          file = open(os.path.join(path, ".gitlab-ci.yml"), "r")
        except FileNotFoundError:
          logger.warning(f"No .gitlab-ci.yml found for repo {repo.name} in branch {branch} under {path}. Skipping.")
          print(f"[red] No pipeline found for repo {repo.name} in branch {branch}. Skipping.[/red]")
          summary[repo.name][branch] = ":x:"
          progress.update(task, advance=1)
          continue
        pipeline = GitlabCIImporter().getPipeline(file)
        file.close()

        """ Only for multiple branches
        jobs_to_delete = []
        for job in pipeline.jobs.values():
          if job.only:
            if type(job.only) == list:
              if branch not in job.only:
                jobs_to_delete.append(job.name)
          if job.exc:
            if type(job.exc) == list:
              if branch in job.exc:
                jobs_to_delete.append(job.name)
        logger.info(f"Deleting jobs {jobs_to_delete} from pipeline of {repo.name} and branch {branch}...")
        for job in jobs_to_delete:
          pipeline.delete_job(job)
        """

        new_dependencies, pipeline = changeToUpdatedImages(progress, docker_migration, pipeline)
        dependencies = dependencies.union(new_dependencies)
        # Convert the pipeline to Github Actions format, depending on the number of branches
        if len(branches_to_be_migrated[str(repoID)]) <= 1:
          pipelineConverter = GithubSubTreeConverter(architecture, pipeline, github_repo_prefix[repo.name], repoID,
                                                     compatibleImages=docker_migration.nativeImage, rebuild=rebuild, )
          convertedPipeline = pipelineConverter.parse_pipeline(repo.name, repo.secrets)
          file_path = os.path.join(file_path_base, repo.name + ".yml")
        else:
          pipelineConverter = GithubSubTreeConverter(architecture, pipeline,
                                                     github_repo_prefix[repo.name] + "/" + branch, repoID,
                                                     compatibleImages=docker_migration.nativeImage, rebuild=rebuild, )
          convertedPipeline = pipelineConverter.parse_pipeline(repo.name + "_" + branch, repo.secrets)
          file_path = os.path.join(file_path_base, repo.name + "_" + branch + ".yml")
        print(f"[green]Converted pipeline of {repo.name} and branch {branch}")
        summary[repo.name][branch] = ":white_check_mark:"
        # Write and commit action
        writeStringToFile(file_path, convertedPipeline)
        subtree_repo.git.add(all=True)
        subtree_repo.index.commit(f"Migrated pipeline of {repo.name} and branch {branch} from Gitlab to Github")
        progress.update(task, advance=1)
  docker_migration.write_images_being_migrated()
  print()
  print("[bold]Summary of migration:")
  table = Table("Repository name", "Branch", "Migration successful")
  for repoID in config.repoIDS:
    repo = architecture.get_repo_by_ID(repoID)
    for branch in branches_to_be_migrated[repoID]:
      if branch in summary[repo.name]:
        table.add_row(repo.name, branch, summary[repo.name][branch])
      else:
        table.add_row(repo.name, branch, ":x:")
  console.print(table)
  if dependencies:
    print()
    print("[yellow]During the pipeline migration, dependencies with images from the following repos were detected:")
    for repo in dependencies:
      print(repo)
    print("[yellow]Please migrate them to the new registry as well, before running the actions.")


if __name__ == "__main__":
  gitlabFilePath = ".gitlab-ci.yml"
  githubFilePath = ".main.yml"
  GitlabToGithub(gitlabFilePath, "pipeline", ["GitlabToken", "URL", "ID"])
