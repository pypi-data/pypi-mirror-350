import re

from migrationTool.migration_types import Architecture
from migrationTool.pipelineMigration.GithubConverter import GithubActionConverter
from migrationTool.pipelineMigration.Job import Job


class GithubSubTreeConverter(GithubActionConverter):
  # Specialized converter for Monorepo variant"
  def __init__(self, architecture: Architecture, pipeline, repoPath, repoID, compatibleImages=set(),
               rebuild: bool = False, ):
    """
    Initializes the GithubSubTreeConverter class.
    :param pipeline: Pipeline object
    :param repoNames: IDs mapped to names of the repository
    :param repoPath: IDs mapped to paths to the repository
    """
    super().__init__(architecture, pipeline, compatibleImages=compatibleImages, rebuild=rebuild, repoIDs=[repoID])
    self.repoPath = repoPath
    self.repoID = repoID

  # Check for correct overwriting attribuites
  def parse_pipeline(self, name: str, secrets: list[str]) -> str:
    """
        Parses the pipeline of a subtree Repo and returns it in the converted form as a string.
    :param name: Name of the pipeline
    :param secrets: Secrets to be used in the pipeline
    :return: String of the pipeline
    """
    self.file_change_job_needed = False
    pipelineString = ""
    pipelineString += f"name: {name}\n"
    pipelineString += "on:\n"
    pipelineString += "\tpush:\n"
    pipelineString += "\t\tpaths:\n"
    pipelineString += "\t\t\t- '" + self.repoPath + "/**'\n"
    pipelineString += "\tworkflow_dispatch:\n"
    pipelineString += "env:\n"
    pipelineString += f"\tCI_PROJECT_ID : {self.repoID}\n"
    if secrets:
      for secret in secrets:
        if type(secret) == tuple:
          if secret[0] != "CI_PROJECT_ID":
            pipelineString += f"\t{secret[0]} : " + f"{secret[1]}\n"
        else:
          if secret != "CI_PROJECT_ID":
            pipelineString += (f"\t{secret} : " + "${{ secrets." + f"{secret}" + " }}\n")
    if self.pipeline.variables:
      for var_name, var_value in self.pipeline.variables.items():
        pipelineString += f"\t{var_name} : " + f"{var_value}\n"

    pipelineString += "jobs:\n"
    for _, job in self.pipeline.jobs.items():
      # Check whether a job is only run if a file changes
      file_changes = (job.only and type(job.only) == dict and "changes" in job.only)
      if job.rules:
        for rule in job.rules:
          if "changes" in rule:
            file_changes = True
            break
      if file_changes:
        # If yes, add job to check
        self.file_change_job_needed = True
        pipelineString += self.create_file_change_job()
        break

    # Create jobs for the stages
    pipelineString += self.create_stage_jobs()
    # Parse all the normal jobs
    for job in self.pipeline.jobs:
      pipelineString += self.parse_job(self.pipeline.jobs[job], secrets)
      pipelineString += "\n"
    return self.set_indentation_to_two_spaces(pipelineString)

  def parse_job(self, job: Job, secrets: list[str] = []) -> str:
    """
    Parses a job in a subtree repo pipeline and returns it in the converted form as a string.
    :param job: Job object
    :param secrets: List of secrets to be used in the job
    :return: Converted job
    """
    # Uses the normal githubaction converter to parse the job
    jobString = super().parse_job(job, secrets)
    # Add to the cd command in the begining of the commands, so that the job is run in the correct directory
    # Non native job
    jobString = jobString.replace("            cd /workspace\n",
                                  "            cd /workspace\n" + "            cd " + f"{self.repoPath}" + "\n", )
    # Native job, match with begining of run block and prepend cd to folder
    patternRepo = r"(- name: Script\s+run: \|)"
    repoCD = r"\1\n" + f"            cd {self.repoPath}"
    jobString = re.sub(patternRepo, repoCD, jobString)

    # Add the prefix to the paths in the artifact upload bloxks
    artifactUploadPattern = (r"(- name: .*\n\s+uses: actions/upload-artifact@v4\n(?:\s+if: .*\n)?\s+with:\n("
                             r"?:\s+.+\n)*\s+path: \|\n((?:\s+.+\n?)+))")
    prefix = f"{self.repoPath}/"

    def replace_paths_with_prefix(match):
      full_block = match.group(1)
      paths = match.group(2).splitlines()
      prefixed_paths = [f"            {prefix}{path.strip()}" for path in paths if path.strip()]
      full_block_without_path = re.sub(r"path: \|.*", "", full_block, flags=re.DOTALL)
      return (full_block_without_path + "path: |\n" + "\n".join(prefixed_paths) + "\n")

    jobString = re.sub(artifactUploadPattern, replace_paths_with_prefix, jobString)

    # Add the prefix to the paths in the artifact download blocks
    artifactDownloadPattern = (r"(- name: .*\n\s+uses: actions/download-artifact@v4\n(?:\s+.+\n)*?\s+path: \|\n)(("
                               r"?:\s+.+\n?)+?)")
    jobString = re.sub(artifactDownloadPattern, replace_paths_with_prefix, jobString)

    # Add the prefix to the paths in the upload pages blocks
    uploadPagesPattern = r"(- name: Upload Pages\s+uses: actions/upload-pages-artifact@v3\s+with:\s+path: )(.+)"

    def add_prefix_to_upload_pages_path(match):
      full_block = match.group(1)  # Der Block bis einschließlich `path:`
      path_value = match.group(2).strip()  # Der ursprüngliche `path`-Wert
      return full_block + prefix + path_value  # Präfix hinzufügen

    jobString = re.sub(uploadPagesPattern, add_prefix_to_upload_pages_path, jobString)

    if job.trigger:
      url_pattern = (r"https://api\.github\.com/repos/\$\{\{\s*github\.repository_owner\s*\}\}/(["
                     r"^/]+)/actions/workflows/([^/]+)\.yml/dispatches")
      ref_pattern = r"-d\s+'\{\"ref\":\s*\"([^\"]+)\"\}'"

      triggered_repo = job.trigger["project"].split("/")[-1]
      repo = self.architecture.get_repo_by_name(triggered_repo)
      if repo:
        multiple_branches = True if len(repo.get_branches_to_be_migrated()) > 1 else False
      else:
        multiple_branches = False

      if multiple_branches:
        workloflow_name = triggered_repo + "_" + job.trigger["branch"]
      else:
        workloflow_name = triggered_repo

      jobString = re.sub(url_pattern, fr"https://api.github.com/repos/${{{{ github.repository }}}}/actions/workflows/"
                                      fr"{workloflow_name}.yml/dispatches", jobString)

      # Replace branch name in ref
      # jobString = re.sub(ref_pattern, fr"-d '{{"ref":\"${{{{ github.event.repository.default_branch }}}}\"}}'",
      #                   jobString)

      jobString = re.sub(ref_pattern, "-d '{\"ref\":\"${{ github.event.repository.default_branch }}\"}'", jobString)
    return jobString
