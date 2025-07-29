import logging
import os

import git
import requests
from git import RemoteProgress, GitCommandError
from github import Auth, GithubException, Github
from rich import print
from rich.console import Console
from rich.prompt import Confirm
from rich.table import Table
from tqdm import tqdm

from migrationTool.gitMigration.Git import Git
from migrationTool.gitMigration.Uploader import Uploader
from migrationTool.migration_types import Architecture, Config

logger = logging.getLogger(__name__)


class GithubUploader(Git, Uploader):
  def __init__(self, config: Config, architecture: Architecture, sourceURL="https://api.github.com", ):
    super().__init__()
    Uploader.__init__(self, config, architecture)
    auth = Auth.Token(self.config.targetToken)
    self.g = Github(auth=auth, base_url=sourceURL)

  def create_private_repo(self, name):
    """
    Create a private repository on the target Git instance.
    :param name: Name of the repository to be created
    :return: Repository object
    """
    try:
      repo = self.g.get_user().create_repo(name, private=True)
    except GithubException as e:
      if e.status == 422:
        logger.info(f"Repository '{name}' already exists.")
        repo = self.g.get_user().get_repo(name)
        if Confirm.ask(f"[red] Delete existing Repo {name}"):
          repo.delete()
          logger.info(f"Repository '{name}' deleted.")
          repo = self.g.get_user().create_repo(name, private=True)
          logger.info(f"New repository '{name}' created.")
        else:
          logger.info(f"Keeping existing repository '{name}'.")
          repo = self.g.get_user().get_repo(name)
      else:
        raise
    return repo

  def create_public_repo(self, name):
    """
    Create a public repository on the target Git instance.
    :param name: Name of the repository to be created
    :return: Repository object
    """
    try:
      repo = self.g.get_user().create_repo(name, private=False)
    except GithubException as e:
      if e.status == 422:
        logger.info(f"Repository '{name}' already exists.")
        repo = self.g.get_user().get_repo(name)
        if Confirm.ask("[red]Delete existing repository?"):
          repo.delete()
          logger.info(f"Repository '{name}' deleted.")
          repo = self.g.get_user().create_repo(name, private=False)
          logger.info(f"New repository '{name}' created.")
        else:
          logger.info(f"Keeping existing repository '{name}'.")
          repo = self.g.get_user().get_repo(name)
      else:
        raise
    return repo

  def get_or_create_remote_repo(self, name):
    """
    Get or create a repository on the target Git instance.
    :param name: Name of the repository to be created
    :return: Repository object
    """
    try:
      if "/" in name:
        repo = self.g.get_repo(name)
      else:
        repo = self.g.get_user().get_repo(name)
      logger.info(f"Repository '{name}' already exists on remote.")
      print(f"[yellow]Repository '{name}' already exists on remote.[/yellow]")
      if Confirm.ask("[red]Delete existing repository "):
        if Confirm.ask("[red]Are you sure?"):
          repo.delete()
          logger.info(f"Repository '{name}' deleted.")
          if Confirm.ask("Create new public repo? Otherwise it will be private"):
            repo = self.create_public_repo(name)
          else:
            repo = self.create_private_repo(name)
          logger.info(f"New repository '{name}' created.")
    except GithubException as e:
      if e.status == 404:
        print(f"[yellow]Repository '{name}' does not exist on GitHub.[/yellow]")
        logger.info(f"Repository '{name}' does not exist.")
        if Confirm.ask("Create new public repo? Otherwise it will be private "):
          repo = self.create_public_repo(name)
        else:
          repo = self.create_private_repo(name)
      else:
        raise
    return repo

  def create_secrets(self, github_repo, secrets):
    """
    Create secrets for the repository on the target Git instance. If a secret already exists, it is not changed.
    :param github_repo: Github repo object
    :param secrets: secrets to be created
    :return:
    """
    existing_secrets = list(github_repo.get_secrets("actions"))
    existing_secrets = [secret.name for secret in existing_secrets]
    if existing_secrets:
      logger.info("Existing secrets in the GitHub Repo: " + str(existing_secrets))
      print("Existing secrets in the GitHub Repo: ", existing_secrets)
    for name, secret in secrets.items():
      if name in existing_secrets:
        logger.info(f"Secret '{name}' already exists. Skipping creation.")
        continue
      else:
        github_repo.create_secret(name, secret)
        logger.info(f"Secret '{name}' created successfully.")
        print(f"Secret '{name}' created successfully.")

  def list_private_repos(self):
    """
    List all private repositories on the target Git instance.
    :return: List of repository names
    """
    repos = self.g.get_user().get_repos(public=False)
    return [repo.name for repo in repos if repo.private]

  def list_public_repos(self):
    """
    List all private repositories on the target Git instance.
    :return: List of repository names
    """
    repos = self.g.get_user().get_repos(public=True)
    return [repo.name for repo in repos if repo.private]

  # ToDo: Rework to current design
  def upload_repo(self, repoID, disable_scanning=False):
    """
    Upload a repository to the target Git instance.
    :param repoID: RepositoryID to be uploaded
    :param secrets: secrets to be created
    :param disable_scanning: Whether to disable push protection in this repo
    """
    logger = logging.getLogger(__name__)
    print(logger.handlers)
    repo = self.architecture.get_repo_by_ID(repoID)
    path = os.path.join(os.getcwd(), "repos", repo.name)
    repo_git = repo.get_repo()
    logger.info(f"Uploading {repo.name} to the target Git instance...")
    # self.set_upstream_for_branches(repo)
    github_repo = self.get_or_create_remote_repo(repo.name)
    if disable_scanning or True:
      self.deactivate_push_protection(github_repo)
    self.create_secrets(github_repo, repo.secrets)

    existing_branches = [b.name for b in github_repo.get_branches()]
    remote_url = github_repo.clone_url.replace("https://", f"https://{self.config.targetToken}@")
    self.reset_remote_origin(repo_git, remote_url)
    for branch in repo.get_branches_to_be_migrated():
      if branch in existing_branches and branch != "master":
        logger.info(f"Branch {branch} already exists in the target repository.")
      else:
        logger.info(f"Uploading {branch} branch...")
        with PushProgress() as progress:
          a = repo_git.remote(name="origin").push(refspec=f"{branch}:{branch}", force=True, progress=progress)
          if a:
            print(a[0].summary)
            print(a[0].flags)
            print(a[0].remote_ref_string)
            print()
        logger.info(f"Branch {branch} uploaded successfully.")
    if disable_scanning or True:
      self.activate_push_protection(github_repo)
    github_repo.edit(default_branch="master")

  def get_monorepo_secrets(self):
    """
    Get secrets for the monorepo
    :return: Secrets for the monorepo
    """
    secrets = {}
    for repoID in self.config.repoIDS:
      repo = self.architecture.get_repo_by_ID(repoID)
      for name, value in repo.secrets_to_create:
        if name not in secrets.keys():
          secrets[name] = value
        elif secrets[name] != value:
          logger.warning(f"Secret {name} defined multiple times with different values in architecture.yaml.")
    return secrets

  def upload_mono_repo(self, disable_scanning=False):
    """
    Upload a monorepo with multiple subtreesa to the target Git instance.
    :param monorepo_name: Repo Object
    :param secrets: Secrets to be created
    :param disable_scanning: Whether to disable push protection in this repo
    """

    try:
      if "/" in self.config.monorepoName:
        path = os.path.join(os.getcwd(), "repos", self.config.monorepoName.split("/")[1])
        monorepo_name = self.config.monorepoName.split("/")[1]
      else:
        path = os.path.join(os.getcwd(), "repos", self.config.monorepoName)
        monorepo_name = self.config.monorepoName
      local_repo = git.Repo(path)
      logger.info(f"Local repo path: {path}")
      print(f"Local repo path: {path}")
    except git.exc.InvalidGitRepositoryError:
      logger.error(f"The monorepo '{self.config.monorepoName}' does not exist.")
      exit(1)
    # Config needed to push large files
    # local_repo.git.config('http.postBuffer', '524288000', local=True)
    logger.info(f"Uploading {monorepo_name} to the {monorepo_name}...")
    github_repo = self.get_or_create_remote_repo(self.config.monorepoName)
    if disable_scanning:
      self.deactivate_push_protection(github_repo.url)
    self.create_secrets(github_repo, self.get_monorepo_secrets())
    remote_url = github_repo.clone_url.replace("https://", f"https://{self.config.targetToken}@")
    self.reset_remote_origin(local_repo, remote_url)

    summary = {}
    existing_branches = [b.name for b in github_repo.get_branches()]
    for branch in local_repo.branches:
      if branch.name in existing_branches:
        if branch.name == "master":
          logger.info(f"Branch {branch.name} skipped as it already exists.")
          continue
        logger.info(f"Branch {branch.name} already exists in the target repository.")
        print(f"[red]Branch {branch.name} already exists in the target repository.[/red]")
        if not Confirm.ask("Still try to upload? This will override the existing history: "):
          print("[red]Skipping branch upload...[/red]")
          logger.info(f"Skipping branch {branch.name}.")
          continue
        else:
          logger.warning("Forcing update of branch {branch.name}...")
          print("[yellow]Forcing update of branch {branch.name}...[/yellow]")
      print(f"Pushing branch {branch.name}...")
      try:
        local_repo.git.checkout(branch.name)
      except git.exc.GitCommandError as e:
        logger.error(f"Branch {branch.name} could not be checked out, skipping" + str(e))
        print(f"[red]Branch {branch.name} could not be checked out, skipping[/red]")
        continue

      summary[branch.name] = self.push_subtree_wise(branch, local_repo)
      if branch.name == "master":
        github_repo.edit(default_branch="master")
        logger.info(f"master branch set as default branch.")

    # Different upload strategies
    # self.branchWiseUpload(existing_branches, local_repo)
    # self.commitWiseUpload(existing_branches, local_repo)
    if disable_scanning:
      self.activate_push_protection(github_repo.url)

    print()
    console = Console()
    table = Table("Branch", "Push status")
    for branch, status in summary.items():
      table.add_row(branch, status)
    console.print(table)

  def push_subtree_wise(self, branch, local_repo):
    """
        Upload one subtree after another in chronological order.
    :param branch: Branch to be uploaded
    :param local_repo: local repository object
    """
    # Commit one subtree after another
    commits = list(local_repo.iter_commits(branch))
    commits.reverse()
    pushList = []
    for commit in commits:
      # Get all commits in which a subtree was added
      if "subtree" in commit.message.lower():
        pushList.append(commit)
    for i, push in enumerate(pushList):
      # Push all those commits in chronological order
      logger.info(f"Pushing SHA:{push.hexsha}")
      with PushProgress() as progress:
        a = None
        try:
          a = local_repo.remote(name="origin").push(refspec=f"{push.hexsha}:refs/heads/{branch.name}",
                                                    progress=progress, force=True, )
        except GitCommandError as e:
          logger.error(f"Error pushing {push.hexsha}" + str(e))
          print(f"[red]Error pushing {push.hexsha}[/red]")
          return ":x:"
      # a = local_repo.remote(name="origin").push(refspec=f"{push.hexsha}:refs/heads/{branch.name}")
      if a:
        print(f"[red]Error pushing {push.hexsha}[/red]")
        logger.error(f"Error pushing {push.hexsha}")
        logger.error(a[0].summary)
        logger.error(a[0].flags)
        logger.error(a[0].remote_ref_string)
        return ":x:"

      logger.info(f"Pushed {i + 1} / {len(pushList)} subtrees")
      print(f"Pushed {i + 1} / {len(pushList)} subtrees")
    with PushProgress() as progress:
      a = local_repo.remote(name="origin").push(refspec=f"{branch.name}:{branch.name}", force=True, progress=progress)
    logger.info(f"Sucessfully pushed {branch.name} branch")
    print(f"[green]Sucessfully pushed {branch.name} branch[/green]")
    return ":white_check_mark:"

  def push_branch_wise(self, existingBranches, localRepo):
    """
        Push whole branches after one another
    :param existingBranches: Branches already existing in github repo, are skipped
    :param localRepo: local repository object
    """
    for branch in localRepo.branches:
      if branch.name in existingBranches:
        logger.info(f"Branch {branch.name} already exists in the target repository.")
      else:
        logger.info(f"Uploading {branch.name} branch...")
        with PushProgress() as progress:
          a = localRepo.remote(name="origin").push(refspec=f"{branch.name}:{branch.name}", force=True,
                                                   progress=progress, )
          if a:
            print(a[0].summary)
            print(a[0].flags)
            print(a[0].remote_ref_string)
            print()
        logger.info(f"Branch {branch.name} uploaded successfully.")

  def push_commit_wise(self, existingBranches, localRepo):
    """
        Push all commits of a branch in chronological order
    :param existingBranches: Branches existing in the github repo are skipped
    :param localRepo: local repository object
    """
    for branch in localRepo.branches:
      if branch.name in existingBranches:
        logger.info(f"Branch {branch.name} already exists in the target repository.")
      else:
        logger.info(f"Uploading {branch.name} branch commit by commit...")
        commits = list(localRepo.iter_commits(branch.name, reverse=True))  # Commits in chronologischer Reihenfolge

        with tqdm(total=len(commits), desc=f"Commits in {branch.name}", unit="commit") as commit_pbar:
          for commit in commits:
            localRepo.git.checkout(branch.name)
            localRepo.git.reset("--hard", commit.hexsha)  # Setze den Branch auf den aktuellen Commit
            a = localRepo.remote(name="origin").push(refspec=f"{branch.name}:{branch.name}", force=True)
            commit_pbar.update(1)

  def deactivate_push_protection(self, url):
    """
        Deactivates push protection for the given GitHub repository.
    :param url: URL to Github repository API
    :return:
    """
    headers = {"Accept": "application/vnd.github+json", "Authorization": f"Bearer {self.config.targetToken}",
               "X-GitHub-Api-Version": "2022-11-28", }
    payload = {"security_and_analysis": {"secret_scanning_push_protection": {"status": "disabled"}, }}

    response = requests.patch(url, headers=headers, json=payload)
    if response.status_code == 200:
      logger.info("Push protection deactivated successfully.")
      print("[green]Push protection deactivated successfully.")
    else:
      logger.warning(
        "Push protection deactivation failed. Push might not be possible. Either deactivate manually or push manually "
        "and remove blocked blobs.")
      print("[red]Push protection deactivation failed. Push might not be possible. Either deactivate manually or push "
            "manually and remove blocked blobs.")

  def activate_push_protection(self, url):
    """
        Activates Push Protection for the given GitHub repository.
    :param url: URL to Github repository API
    """
    headers = {"Accept": "application/vnd.github+json", "Authorization": f"Bearer {self.config.targetToken}",
               "X-GitHub-Api-Version": "2022-11-28", }
    payload = {"security_and_analysis": {"secret_scanning_push_protection": {"status": "enabled"}, }}

    response = requests.patch(url, headers=headers, json=payload)
    if response.status_code == 200:
      logger.info("Push protection activated successfully.")
      print("[green]Push protection activated successfully.")
    else:
      logger.warning("Push protection activation failed.")
      print("[red]Push protection activation failed.")

  # ToDo: Remove once MonoRepo variant is tested If needed migrate to new architecture
  """
def dockerImageMigration(self, architecture, repoID):
    images = ",".join(architecture[repoID]["DockerImages"])
    action = "name: Migrate Docker Images\n"
    action += "on:\n"
    action += "  workflow_dispatch:\n"
    action += "jobs:\n"
    action += "  docker-migration:\n"
    action += "    runs-on: ubuntu-latest\n"
    action += "    env:\n"
    action += f'      GITLAB_USERNAME: "{self.config.sourceUser}"\n'
    action += "      GITLABTOKEN: ${{ secrets.GITLABTOKEN }}\n"
    action += f'      GITLAB_REPO: "{(architecture[repoID]["Namespace"] + "/" + architecture[repoID]["Name"]).lower(
    )}"\n'
    action += f'      IMAGES_LIST: "{images}"\n'
    action += "      GHCR_PAT: ${{ secrets.GHCR_PAT }}\n"
    action += '      GHCR_REPO_OWNER: "davidblm"\n'
    action += "    steps:\n"
    action += "      - name: Log in to GitLab\n"
    action += "        run: |\n"
    action += '          docker login https://git.rwth-aachen.de/ -u "$GITLAB_USERNAME" -p "$GITLABTOKEN"\n'
    action += "      - name: Log in to GitHub\n"
    action += "        run: |\n"
    action += '          echo "${{ secrets.GITHUB_TOKEN }}" | docker login ghcr.io -u "${{ github.actor }}" 
    --password-stdin\n'
    action += "      - name: Migrate Docker images\n"
    action += "        run: |\n"
    action += '          IFS="," read -ra IMAGES <<< "$IMAGES_LIST"\n'
    action += '          for IMAGE in "${IMAGES[@]}"; do\n'
    action += '            GITLAB_IMAGE="registry.git.rwth-aachen.de/$GITLAB_REPO/$IMAGE"\n'
    action += '            LOWERCASE_IMAGE=$(echo "$IMAGE" | tr "[:upper:]" "[:lower:]")\n'
    action += '            GHCR_IMAGE="ghcr.io/$GHCR_REPO_OWNER/$LOWERCASE_IMAGE"\n'
    action += '            echo "Pulling image from GitLab: $GITLAB_IMAGE"\n'
    action += '            docker pull "$GITLAB_IMAGE"\n'
    action += '            echo "Tagging image for GHCR: $GHCR_IMAGE"\n'
    action += '            docker tag "$GITLAB_IMAGE" "$GHCR_IMAGE"\n'
    action += '            echo "Pushing image to GHCR: $GHCR_IMAGE"\n'
    action += '            docker push "$GHCR_IMAGE"\n'
    action += '            echo "Removing local image: $GHCR_IMAGE"\n'
    action += '            docker rmi -f $(docker images -q) || true\n'
    action += '          done\n'

    file_path = f"repos/{architecture[repoID]["Name"]}/.github/workflows/image.yml"
    folder_path = os.path.dirname(file_path)

    # Ordner erstellen, falls sie nicht existieren
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Ordner '{folder_path}' wurde erstellt.")

    # Datei schreiben
    with open(file_path, 'w') as file:
        file.write(action)
        print(f"Datei '{file_path}' wurde erfolgreich geschrieben.")
    repo = git.Repo("./repos/" + architecture[repoID]["Name"])
    repo.git.add(all=True)
    repo.index.commit("Added Docker image migration workflow")
"""

  def docker_image_migration_monorepo(self, repos_to_be_migrated=None):
    """
        Adds a new GitHub action to migrate Docker images from GitLab to GitHub.
    :param architecture: Architecture object
    :param repos_to_be_migrated: List of repositories to be migrated. If None, all repositories are migrated.
    :return:
    """
    if repos_to_be_migrated is None:
      repos_to_be_migrated = self.config.repoIDS
    action = "name: Migrate Docker Images\n"
    action += "on:\n"
    action += "  workflow_dispatch:\n"
    action += "jobs:\n"
    action += "  docker-migration:\n"
    action += "    runs-on: ubuntu-latest\n"
    action += "    env:\n"
    action += f'      GITLAB_USERNAME: "{self.config.sourceUser}"\n'
    action += "      GITLABTOKEN: ${{ secrets.GITLABTOKEN }}\n"
    action += "      GHCR_PAT: ${{ secrets.GHCR_PAT }}\n"
    # action += '      GHCR_REPO_OWNER: "davidblm"\n'
    # action += "      GHCR_REPO_OWNER: ${{ github.actor | toLowerCase}}\n" #ToDo: Add automatic username
    action += "    steps:\n"
    action += "      - name: Log in to GitLab\n"
    action += "        run: |\n"
    action += '          docker login https://git.rwth-aachen.de/ -u "$GITLAB_USERNAME" -p "$GITLABTOKEN"\n'
    action += "      - name: Log in to GitHub\n"
    action += "        run: |\n"
    action += ('          echo "${{ secrets.GITHUB_TOKEN }}" | docker login ghcr.io -u "${{ github.actor }}" '
               '--password-stdin\n')
    for repoId in repos_to_be_migrated:
      repo = self.architecture.get_repo_by_ID(repoId)
      images = ",".join(repo.images)
      gitlab_repo = (repo.namespace + "/" + repo.name).lower()
      action += f"      - name: Migrate Docker images from {repo.name}\n"
      action += "        run: |\n"
      action += '          LOWERCASE_OWNER=$(echo "${{ github.repository_owner }}" | tr "[:upper:]" "[:lower:]")\n'
      action += f'          IFS="," read -ra IMAGES <<< "{images}"\n'
      action += '          for IMAGE in "${IMAGES[@]}"; do\n'
      # action += f'            GITLAB_IMAGE="registry.git.rwth-aachen.de/{gitlab_repo}/$IMAGE"\n'
      action += "            if [[ $IMAGE == :* ]]; then\n"
      action += f'              GITLAB_IMAGE="registry.git.rwth-aachen.de/{gitlab_repo}$IMAGE"\n'
      action += "            else\n"
      action += f'              GITLAB_IMAGE="registry.git.rwth-aachen.de/{gitlab_repo}/$IMAGE"\n'
      action += "            fi\n"
      action += '            LOWERCASE_IMAGE=$(echo "$IMAGE" | tr "[:upper:]" "[:lower:]")\n'
      action += "            if [[ $IMAGE == :* ]]; then\n"
      action += f'              GHCR_IMAGE="ghcr.io/$LOWERCASE_OWNER/{repo.name.lower()}$LOWERCASE_IMAGE"\n'
      action += "            else\n"
      action += f'               GHCR_IMAGE="ghcr.io/$LOWERCASE_OWNER/{repo.name.lower()}/$LOWERCASE_IMAGE"\n'
      action += "            fi\n"
      action += '            echo "Pulling image from GitLab: $GITLAB_IMAGE"\n'
      action += '            docker pull "$GITLAB_IMAGE"\n'
      action += '            echo "Tagging image for GHCR: $GHCR_IMAGE"\n'
      action += '            docker tag "$GITLAB_IMAGE" "$GHCR_IMAGE"\n'
      action += '            echo "Pushing image to GHCR: $GHCR_IMAGE"\n'
      action += '            docker push "$GHCR_IMAGE"\n'
      action += '            echo "Removing local image: $GHCR_IMAGE"\n'
      action += "            docker rmi -f $(docker images -q) || true\n"
      action += "          done\n"
    target_repo = self.config.monorepoName
    file_path = os.path.join(os.getcwd(), "repos", target_repo, ".github", "workflows", "image.yml")
    folder_path = os.path.dirname(file_path)
    if not os.path.exists(os.path.join(os.getcwd(), "repos", target_repo)):
      logger.error(f"Repository '{target_repo}' nicht gefunden.")
      exit(1)

    if not os.path.exists(folder_path):
      os.makedirs(folder_path)
      print(f"Ordner '{folder_path}' wurde erstellt.")
    with open(file_path, "w") as file:
      file.write(action)
      print(f"Datei '{file_path}' wurde erfolgreich geschrieben.")
    repo = git.Repo(os.path.join(os.getcwd(), "repos", target_repo))
    repo.git.add(all=True)
    repo.index.commit("Added Docker image migration workflow")


class PushProgress(RemoteProgress):
  def __init__(self):
    super().__init__()
    self.pbar = tqdm(desc="Pushing", unit="objects")

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
