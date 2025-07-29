import logging
import re
from rich import print

from migrationTool.migration_types import Architecture
from migrationTool.pipelineMigration.Converter import Converter
from migrationTool.pipelineMigration.Job import Job
from migrationTool.pipelineMigration.Pipeline import Pipeline

logger = logging.getLogger(__name__)


class GithubActionConverter(Converter):
  """
  This class converts a pipeline Object to GitHub Actions.
  """

  def __init__(self, architecture: Architecture, pipeline: Pipeline, compatibleImages=set(), repoIDs=[],
               rebuild: bool = False):
    """
    Initializes the GithubActionConverter class.
    :param architecture: Architecture object
    :param pipeline: Pipeline object
    :param rebuild: Whether to rebuild the docker images or not
    container
    """

    self.pipeline = pipeline
    self.rebuild = rebuild
    self.timeout = 60  # Default timeout in minutes
    self.architecture = architecture
    if not repoIDs:
      self.repoIDS = architecture.repoIDs
    else:
      self.repoIDs = repoIDs

    """
    # ToDo: Delete for production, implement their import
    self.compatible_images = {"maven:3.6-jdk-8",
                              "registry.git.rwth-aachen.de/monticore/embeddedmontiarc/generators/emadl2cpp"
                              "/dockerimages/mxnet170-onnx:v0.0.1",
                              "registry.git.rwth-aachen.de/monticore/embeddedmontiarc/generators/emadl2cpp"
                              "/dockerimages/tensorflow-onnx:latest",
                              "registry.git.rwth-aachen.de/monticore/embeddedmontiarc/applications/mnistcalculator"
                              "/tensorflow",
                              "registry.git.rwth-aachen.de/monticore/embeddedmontiarc/generators/emadl2cpp/mxnet/190"
                              ":v0.0.2", "registry.git.rwth-aachen.de/monticore/embeddedmontiarc/generators/emadl2cpp"
                                         "/dockerimages/mxnet170:v0.0.1"}
    self.compatible_images = {"maven:3.6-jdk-8"}
    """
    self.compatible_images = compatibleImages

    self.migrated_docker_images = {}
    for repoID in self.repoIDs:
      repo = self.architecture.get_repo_by_ID(repoID)
      for image in repo.images:
        if repo.name not in self.migrated_docker_images:
          self.migrated_docker_images[repo.name] = [image]
        else:
          self.migrated_docker_images[repo.name].append(image)

  def parse_pipeline(self, repoID) -> str:
    """

    :param name: Name of the pipeline
    :param secrets: Secrets to be used in the pipeline, please see architecture.yaml for more information
    :return: String of the converted pipeline
    """
    repo = self.architecture.get_repo_by_ID(repoID)
    self.file_change_job_needed = False  # Whether some jobs are only run if some files changed
    pipeline_string = ""
    pipeline_string += f"name: {repo.name}\n"
    pipeline_string += "on:\n"
    pipeline_string += "\tpush:\n"
    pipeline_string += "\tworkflow_dispatch:\n"
    pipeline_string += "env:\n"
    if repo.secrets:
      for secret in repo.secrets:
        if type(secret) == tuple:
          pipeline_string += f"\t{secret[0]} : " + f"{secret[1]}\n"
        else:
          pipeline_string += f"\t{secret} : " + "${{ secrets." + f"{secret}" + " }}\n"
    if self.pipeline.variables:
      for var_name, var_value in self.pipeline.variables.items():
        pipeline_string += f"\t{var_name} : " + f"{var_value}\n"

    pipeline_string += "jobs:\n"
    # Check if job(s) exist that are only run if certain files changed
    for _, job in self.pipeline.jobs.items():
      # Check whether a job is only run if a file changes
      needed = job.only and type(job.only) == dict and "changes" in job.only
      if job.rules:
        for rule in job.rules:
          if "changes" in rule:
            needed = True
            break
      if needed:
        pipeline_string += self.create_file_change_job()
        self.file_change_job_needed = True
        break

    # Create jobs representing each stage
    pipeline_string += self.create_stage_jobs()

    # Parse each regular job of the pipeline
    for job in self.pipeline.jobs:
      pipeline_string += self.parse_job(self.pipeline.jobs[job], repo.secrets)
      pipeline_string += "\n"
    return self.set_indentation_to_two_spaces(pipeline_string)

  def parse_job(self, job: Job, secrets: list[str] = []) -> str:
    """
        Converts a single job as part of a whole pipeline to a string.
    :param job: Job object
    :param secrets: Secrets to be used in the job, please see architecture.yaml for more information
    :return: String of this job block
    """
    # Check if the job is native or needs to be run in a separate docker container
    if job.image in self.compatible_images or not job.image:
      native = True
    else:
      native = False

    job_string = ""
    job_string += f"\t{job.name.replace("/", "_").replace(" ", "_")}:\n"
    # Checks the needs of the job and sets the needs of the job accordingly
    if job.needs:
      # If needs exist add them
      job_string += (f"\t\tneeds: ")
      if len(job.needs) == 1:
        job_string += f"{job.needs[0].replace("/", "_").replace(" ", "_")}\n"
      else:
        for i, j in enumerate(job.needs):
          if i == 0:
            job_string += (f"[ {j.replace("/", "_").replace(" ", "_")} ")
          else:
            job_string += (f", {j.replace("/", "_").replace(" ", "_")}")
        job_string += (f"]\n")
    else:
      # If no needs exist, check if the job is the first in the pipeline
      i = self.pipeline.stages.index(job.stage)
      if i > 0:
        # If not the first job, add the previous stage as a need
        job_string += f"\t\tneeds: {self.pipeline.schedule[i - 1].replace('/', '_').replace(' ', '_') + "_phase"}\n"
      else:
        # If first job, check if the file change job is needed and add it as need
        if self.file_change_job_needed:
          job_string += f"\t\tneeds: FileChanges\n"

    # Construct the if condition for whether this job should be run
    job_string += self.if_condition(job)

    # Per default all jobs run on an ubuntu runner
    job_string += f"\t\truns-on: ubuntu-latest\n"

    # If image can be run natively and a special docker image was provided add the container block
    if native and job.image:
      job_string += f"\t\tcontainer:\n"
      job_string += f"\t\t\timage: {job.image}\n"

    job_string += f"\t\ttimeout-minutes: {self.timeout}\n"

    # If the job publishes to pages it needs special permissions
    if job.artifacts:
      if job.artifacts["paths"] == ["public"] and job.name == "pages":
        job_string += f"\t\tpermissions:\n"
        job_string += f"\t\t\tpages: write\n"
        job_string += f"\t\t\tid-token: write\n"

    # Add the steps block
    job_string += f"\t\tsteps:\n"
    # First chekout only latest version of the repo
    job_string += GithubActionConverter.add_checkout_step()

    # If necessary restore the splitted large files
    if self.rebuild:
      job_string += GithubActionConverter.restore_large_files_step()

    # If the job has needs, which uploaded artifacts download them
    if job.needs:
      for need in job.needs:
        if self.pipeline.jobs[need].artifacts:
          job_string += GithubActionConverter.download_artifacts(self.pipeline.jobs[need].artifacts["paths"],
                                                                 need.replace("/", "_").replace(" ", "_"))

    # If the job is not native, start the separate docker container
    if not native:
      job_string += GithubActionConverter.start_docker_container(job.image, secrets, "")

    # ToDo: Test trigger, implement check, that triggered jobs exist
    if job.trigger:
      # If the job is a trigger job, add the trigger block
      repo_name = job.trigger["project"].split("/")[-1]
      branch = job.trigger["branch"]

      triggered_repo = self.architecture.get_repo_by_name(repo_name)
      if triggered_repo is None:
        print(f"[red] The repo {repo_name} has not been migrated yet!")
      elif branch not in triggered_repo.get_branches_to_be_migrated():
        print(
          f"[red] The branch {branch} of {repo_name} has not been part of the migration yet!")  # If the repo is not
        # in the monorepo, add the checkout step
      job_string += GithubActionConverter.add_checkout_step(repo_name)
      job_string += GithubActionConverter.trigger(repo_name, branch)

    elif job.script:
      # Add the script the job should run
      if native:
        # If native the script can be run directly
        job_string += f"\t\t\t- name: Script\n"
        if job.allowFailure == True:
          job_string += "\t\t\t\tcontinue-on-error: true\n"
        job_string += f"\t\t\t\trun: |\n"
        job.script = self.script_parser(job.script)
        for command in job.script:
          job_string += f"\t\t\t\t\t\t{command}\n"
      else:
        # If not native, the script needs to be run in the docker container using docker exec
        job_string += f"\t\t\t- name: Script\n"
        if job.allowFailure == True:
          job_string += "\t\t\t\tcontinue-on-error: true\n"
        # Create a SCRIPT variable that contains the script
        job_string += f"\t\t\t\tenv:\n"
        job_string += f"\t\t\t\t\tSCRIPT: |\n"
        job_string += f"\t\t\t\t\t\tcd /workspace\n"
        job.script = self.script_parser(job.script)
        for command in job.script:
          job_string += f"\t\t\t\t\t\t{command}\n"
        # Run this script in the docker container
        job_string += f'\t\t\t\trun: docker exec build-container bash -c "$SCRIPT"\n'

      # Once the script is done and the job was successful, upload the artifacts
      if job.artifacts:
        if job.artifacts["paths"] == ["public"] and job.name == "pages":
          # If the job is a pages job, deploy the pages
          job_string += GithubActionConverter.deploy_pages(job.artifacts["paths"][0])
        else:
          if "expire_in" in job.artifacts:
            retention_time = job.artifacts["expire_in"].replace("day", "")
          else:
            retention_time = 7
          if "when" in job.artifacts:
            if job.artifacts["when"] == "always":
              # Upload the artifacts always
              when = "always()"
            else:
              # Upload only if successful
              when = "success()"
          else:
            when = "success()"

          # If the job is not a pages job, upload the artifacts normally
          job_string += GithubActionConverter.upload_artifacs(job.artifacts["paths"],
                                                              job.name.replace("/", "_").replace(" ", "_"), when,
                                                              retention_time)
    return Converter.set_indentation_to_two_spaces(job_string)

  @staticmethod
  def add_checkout_step(repo: str = "", depth=1) -> str:
    """
        Returns the block for the Github Actions checkout step.
    :param repo: Name of the repo to be checked out. If empty, the current repo is checked out
    :param depth: Number of commits to be checked out. Default 1 = only the latest commit
    :return: String of the checkout step
    """
    checkout = ""
    checkout += f"\t\t\t- name: Checkout latest commit\n"
    checkout += f"\t\t\t\tuses: actions/checkout@v4\n"
    checkout += f"\t\t\t\twith:\n"
    checkout += f"\t\t\t\t\tfetch-depth: {depth}\n"
    if repo:
      checkout += f"\t\t\t\t\trepository: {repo}\n"
      checkout += "\t\t\t\t\ttoken: ${{ secrets.ACCESS_TOKEN }}\n"
    return checkout

  @staticmethod
  def add_checkout_step_manual(repo: str = "${{ github.repository }}") -> str:
    """
        Experimental function: Checkout the repo manually using git clone. Should not be used
    :param repo: Name of the repo to be checked out. If empty, the current repo is checked out
    :return: String of the manual checkout step
    """
    checkout = ""
    checkout += f"\t\t\t- name: Checkout latest commit\n"
    checkout += f"\t\t\t\trun: |\n"
    checkout += "\t\t\t\t\tgit clone --depth 1 " + ("https://${{github.REPOSITORY_OWNER}}:${{ secrets.ACCESS_TOKEN "
                                                    "}}@github.com/") + f"{repo} repo\n"
    checkout += f"\t\t\t\t\tcd repo\n"
    checkout += f"\t\t\t\t\tls\n"
    return checkout

  @staticmethod
  def restore_large_files_step() -> str:
    """
        Returns the block for restoring large files that were split into parts.
    :return: String of the restore step
    """
    restore = ""
    restore += f"\t\t\t- name: Restore large files\n"
    restore += f"\t\t\t\trun: |\n"
    restore += "\t\t\t\t\tls\n"
    restore += f"\t\t\t\t\tfind . -type f -name '*.part*' | sort | while read part; do\n"
    restore += f"\t\t\t\t\techo \"Restoring $part\"\n"
    restore += f"\t\t\t\t\tbase=$(echo \"$part\" | sed 's/.part.*//')\n"
    restore += f"\t\t\t\t\tcat \"$part\" >> \"$base\"\n"
    restore += f"\t\t\t\t\trm \"$part\"\n"
    restore += f"\t\t\t\t\tdone\n"
    return restore

  @staticmethod
  def start_docker_container(image: str, secrets: list[str], options: str) -> str:
    """
        Returns the block for starting a separate docker container.
    :param image: URL to Image to be used. If the image is in the ghcr.io registry, the GITHUB_TOKEN is used to
    authenticate
    :param secrets: Secrets to be passed into the container.
    :param options: Additional options to be passed to the docker run command
    :return: String of the start block
    """
    start = ""
    start += f"\t\t\t- name: Start Docker Container\n"
    start += f"\t\t\t\trun: |\n"
    if "ghcr.io" in image:
      # ToDo: Change to github repo owner
      start += ('\t\t\t\t\techo "${{ secrets.GITHUB_TOKEN }}" | docker login ghcr.io -u "${{ github.actor }}" '
                '--password-stdin\n')
    start += f"\t\t\t\t\tdocker pull {image.lower()}\n"
    start += f"\t\t\t\t\tdocker run --name build-container -d -v $(pwd):/workspace --network=host {options}"
    for secret in secrets:
      if type(secret) == str:
        if secret != "CI_PROJECT_ID":
          # Add Github secret as environment variable
          start += f" -e {secret}=$" + "{{ secrets." + f"{secret}" + " }}"
        else:
          start += f" -e {secret}=${secret}"
      else:
        # Add environment variable for a variable that is not a secret
        start += f" -e {secret[0]}=${secret[0]}"
    start += f" {image.lower()} tail -f /dev/null\n"
    return start

  @staticmethod
  def upload_artifacs(paths: list[str], name, when="success()", expiration: int = 7) -> str:
    """
        Creates the string for the upload artifacts action block.
    :param paths: Paths to the artifacts to be uploaded
    :param name: Name of the artifact. Must be unique in the workflow
    :param expiration: Optional expiration time in days. Default is 7 days
    :return: String of the upload block
    """
    upload = ""
    upload += f"\t\t\t- name: Upload artifacts\n"
    upload += f"\t\t\t\tuses: actions/upload-artifact@v4\n"
    upload += f"\t\t\t\tif: {when}\n"
    upload += f"\t\t\t\twith:\n"
    upload += f'\t\t\t\t\tname: {name}\n'
    upload += f"\t\t\t\t\tretention-days: {expiration}\n"
    upload += f"\t\t\t\t\tpath: |\n"
    for path in paths:
      upload += f"\t\t\t\t\t\t{path}\n"
    return upload

  @staticmethod
  def download_artifacts(paths: list[str], name) -> str:
    """
        Creates the string for the download artifacts action block.
    :param paths: Paths where the artifacts shall be downloaded to
    :param name: Name of the artifact to be downloaded
    :return: String of the download block
    """
    download = ""
    download += f"\t\t\t- name: Download artifacts\n"
    download += f"\t\t\t\tuses: actions/download-artifact@v4\n"
    download += f"\t\t\t\twith:\n"
    download += f"\t\t\t\t\tname: {name}\n"
    download += f"\t\t\t\t\tpath: |\n"
    for path in paths:
      download += f"\t\t\t\t\t\t{path}\n"
    return download

  @staticmethod
  def deploy_pages(path: str) -> str:
    """
        Creates the string for the deploy pages action block.
    :param path: Path to the pages to be deployed
    :return: String of the deploy block
    """
    deploy = ""
    deploy += "\t\t\t- name: Upload Pages\n"
    deploy += "\t\t\t\tuses: actions/upload-pages-artifact@v3\n"
    deploy += "\t\t\t\twith:\n"
    deploy += f"\t\t\t\t\tpath: {path}/\n"
    deploy += "\t\t\t- name: Deploy to Pages\n"
    deploy += "\t\t\t\tuses: actions/deploy-pages@v4\n"
    return deploy

  @staticmethod
  def trigger(repo_name: str, branch: str = "master") -> str:
    """
        Creates the trigger for the pipeline.
    :param repo_name: Name of the repo
    :return: String of the trigger block
    """
    trigger = ""
    trigger += f"\t\t\t- name: Trigger {repo_name} pipeline\n"
    trigger += f"\t\t\t\trun: |\n"
    trigger += f"\t\t\t\t\tcurl -X POST https://api.github.com/repos/${{{{ github.repository_owner }}}}"
    trigger += f"/{repo_name}/actions/workflows/{repo_name}.yml/dispatches \\\n"
    trigger += '\t\t\t\t\t\t-H "Accept: application/vnd.github+json" \\\n'
    trigger += '\t\t\t\t\t\t-H "Authorization: token ${{ secrets.GITHUBTOKEN }}" \\\n'
    trigger += f'\t\t\t\t\t\t-d \'{{"ref": "{branch}"}}\'\n'
    return trigger

  def if_condition(self, job: Job) -> str:
    """
    Creates the if condition for the job.
    :param job: Job object
    :return: String of the if condition
    """
    ifString = ""
    if self.pipeline.stages.index(job.stage) != 0:
      # If the job is not the first job in the pipeline, check if the previous stage was successful
      ifString += "\t\tif: ${{ !cancelled() && !contains(needs.*.result, 'failure') "

    # Handle only keyword
    if job.only:
      if type(job.only) == dict:
        # Job is only to be run if certain files changed
        if "changes" in job.only:
          if ifString == "":
            ifString += "\t\tif: ${{"
          else:
            ifString += " && "
          # Check output of fileChangeJob whether it should be run or skipped
          ifString += f"needs.FileChanges.outputs.run{job.name.replace('/', '_').replace(' ', '_')} == 'true'"

      if type(job.only) == list:
        # Job is only to be run if certain branches are pushed
        if ifString == "":
          ifString += "\t\tif: ${{"
        else:
          ifString += " && "
        for i, branch in enumerate(job.only):
          if i == 0:
            ifString += f" github.ref == 'refs/heads/{branch}'"
          else:
            ifString += f" && github.ref == 'refs/heads/{branch}'"

    # Handle except keyword
    if job.exc:
      # Exclude for single files is not supported automatically
      """
      if type(job.exc) == dict:
          if ifString == "":
              ifString += "\t\tif: ${{"
          # ToDo: Check if this is correct
          if "changes" in job.exc:
              # Job is not to be run if certain files not changed
              ifString += f" && !contains(github.event.head_commit.message, '"
              for i, p in enumerate(job.exc['changes']):
                  if i == 0:
                      ifString += f"{p}"
                  else:
                      ifString += f", {p}"
              ifString += "')"
      """
      # Job is not to be run if certain branches are pushed
      if type(job.exc) == list:
        # Job is not to be run if certain branches are pushed
        for i, branch in enumerate(job.exc):
          if i == 0 and not ifString:
            ifString += f"\t\tif: ${{{{ github.ref != 'refs/heads/{branch}'"
          else:
            ifString += f"\t\t  && github.ref != 'refs/heads/{branch}'"

    if job.rules:
      # Job is only to be run if certain rules are met, which are examined in file changes
      for rule in job.rules:
        if "changes" in rule and "needs.FileChanges" not in ifString:
          if ifString == "":
            ifString += "\t\tif: ${{"
          else:
            ifString += " && "
          # Check output of fileChangeJob whether it should be run or skipped
          ifString += f"needs.FileChanges.outputs.run{job.name.replace('/', '_').replace(' ', '_')} == 'true'"

    if ifString:
      ifString += " }}\n"
    return ifString

  def create_stage_jobs(self):
    """
        Creates a job for each stage in the pipeline.
    :return: String of the stage jobs
    """
    lastStage = ""
    jobString = ""
    # Create a job for each stage in the pipeline, except the last one
    for stage in self.pipeline.schedule[:-1]:

      jobString += f"\t{stage + "_phase:"}\n"

      jobString += f"\t\tneeds: ["
      if lastStage:
        # Add the last stage as need
        jobString += f'{lastStage + "_phase, "}'
      lastStage = stage

      # Add all jobs of the stage as needs
      for i, job in enumerate(self.pipeline.stageJobs[stage]):
        if i == 0:
          jobString += f"{job.replace('/', '_').replace(' ', '_')}"
        else:
          jobString += f", {job.replace('/', '_').replace(' ', '_')}"
      jobString += f"]\n"
      jobString += "\t\tif: ${{ !cancelled()}}\n"
      jobString += f"\t\truns-on: ubuntu-latest\n"
      jobString += "\t\tsteps:\n"
      jobString += f"\t\t\t\t- run: |\n"
      jobString += f'\t\t\t\t\t\techo "Finished stage {stage}"\n'
      jobString += "\t\t\t\t  if: ${{!contains(needs.*.result, 'failure')}}\n"
      jobString += f"\t\t\t\t- run: |\n"
      jobString += f'\t\t\t\t\t\techo "Failed stage {stage}"\n'
      jobString += "\t\t\t\t\t\texit 1\n"
      jobString += "\t\t\t\t  if: ${{contains(needs.*.result, 'failure')}}\n"
    jobString += "\n"
    return jobString

  def create_file_change_job(self):
    """
        Creates a job that checks if certain files changed and sets the output of the job accordingly.
    :return: String of the file change job
    """
    jobString = "\tFileChanges:\n"
    jobString += f"\t\truns-on: ubuntu-latest\n"
    for _, job in self.pipeline.jobs.items():
      job_output_needed = job.only and type(job.only) == dict and "changes" in job.only
      if job.rules:
        for rule in job.rules:
          if "changes" in rule:
            job_output_needed = True
            break
      if job_output_needed:
        jobString += f"\t\toutputs:\n"
        break
    for _, job in self.pipeline.jobs.items():
      # Add an output for each job that is only run if certain files changed
      job_output_needed = job.only and type(job.only) == dict and "changes" in job.only
      if job.rules:
        for rule in job.rules:
          if "changes" in rule:
            job_output_needed = True
            break
      if job_output_needed:
        jobString += (f"\t\t\trun{job.name}: " + "${{" + (f"steps."
                                                          f"{job.name.replace('/', '_').replace(' ', '_')}.outputs.run") + "}}\n")

    jobString += "\t\tsteps:\n"
    # Checkout the last 2 commits
    jobString += self.add_checkout_step(depth=2)
    jobString += f"\t\t\t- name: Check for file changes\n"
    jobString += f"\t\t\t\trun: |\n"
    # Get git diff
    jobString += f"\t\t\t\t\tCHANGES=$(git diff --name-only HEAD^ HEAD)\n"
    jobString += '\t\t\t\t\techo "$CHANGES"\n'
    jobString += '\t\t\t\t\techo "$CHANGES" > diff.txt\n'
    for _, job in self.pipeline.jobs.items():
      job_output_needed = job.only and type(job.only) == dict and "changes" in job.only
      if job.rules:
        for rule in job.rules:
          if "changes" in rule:
            job_output_needed = True
            break
      if job_output_needed:
        # Create a step for each job, whose run condition needs to be checked
        jobString += f"\t\t\t- name: Check {job.name}\n"
        jobString += f"\t\t\t\tid: {job.name.replace('/', '_').replace(' ', '_')}\n"
        jobString += f"\t\t\t\trun: |\n"
        """
        jobString += "\t\t\t\t\trun=false\n"
        for path in job.only["changes"]:
          jobString += "\t\t\t\t\tif cat diff.txt | grep" + f" '^.*{path.replace("/**/*", "")}'" + "; then\n"
          jobString += '\t\t\t\t\t\techo "RUN"\n'
          jobString += "\t\t\t\t\t\trun=true\n"
          jobString += "\t\t\t\t\telse\n"
          jobString += '\t\t\t\t\t\techo "DONT RUN"\n'
          jobString += "\t\t\t\t\tfi\n"
        jobString += '\t\t\t\t\techo "run=$run" >> $GITHUB_OUTPUT\n'
        """
        jobString += "\t\t\t\t\trun=false\n"
        jobString += "\t\t\t\t\tfor path in $(cat diff.txt); do\n"
        paths = []
        if job.only:
          if job.only["changes"]:
            for path in job.only["changes"]:
              paths.append(path.replace("/**/*", ""))
        if job.rules:
          for rule in job.rules:
            if "changes" in rule:
              for path in rule["changes"]:
                paths.append(path.replace("/**/*", ""))

        for path in paths:
          jobString += f"\t\t\t\t\t\tif [[ $path == *{path.replace('/**/*', '')}* ]]; then\n"
          jobString += '\t\t\t\t\t\t\techo "Matching path found: $path"\n'
          jobString += '\t\t\t\t\t\t\techo "RUN"\n'
          jobString += "\t\t\t\t\t\t\trun=true\n"
          jobString += "\t\t\t\t\t\t\tbreak\n"
          jobString += "\t\t\t\t\t\tfi\n"
        jobString += "\t\t\t\t\tdone\n"
        jobString += '\t\t\t\t\techo "Final file change run status: $run"\n'
        jobString += '\t\t\t\t\techo "run=$run" >> $GITHUB_OUTPUT\n'
        if job.rules:
          for i, rule in enumerate(job.rules):
            condition = rule["if"]
            # Handle Branch conditions
            pattern = r'(\$CI_COMMIT_BRANCH)\s*(==|!=)\s*"([^"]+)"'
            replacement = r'${{ github.ref }} \2 "refs/heads/\3"'
            condition = re.sub(pattern, replacement, condition)
            # Handle trigger sources
            pattern = r'(\$CI_PIPELINE_SOURCE)\s*(==|!=)\s*"web"'
            replacement = r'${{ github.event_name }} \2 "workflow_dispatch"'
            condition = re.sub(pattern, replacement, condition)
            if "changes" in rule:
              jobString += f"\t\t\t\t\tif [[ {condition} && $run ]]; then\n"
              jobString += f'\t\t\t\t\t\techo "RUN condition {i} matched"\n'
              jobString += '\t\t\t\t\t\techo "run=true" >> $GITHUB_OUTPUT\n'
              jobString += "\t\t\t\t\t\texit 0\n"
              jobString += "\t\t\t\t\tfi\n"
            else:
              jobString += f"\t\t\t\t\tif [[ {condition} ]]; then\n"
              jobString += f'\t\t\t\t\t\techo "RUN condition {i} matched"\n'
              jobString += '\t\t\t\t\t\techo "run=true" >> $GITHUB_OUTPUT\n'
              jobString += "\t\t\t\t\t\texit 0\n"
              jobString += "\t\t\t\t\tfi\n"
          jobString += '\t\t\t\t\techo "No matching condition found"\n'
          jobString += '\t\t\t\t\t\techo "run=false" >> $GITHUB_OUTPUT\n'
    return jobString

  def script_parser(self, script: list[str]) -> list[str]:
    """
    Parses the script of a job and returns it as a string. Can be overridden by subclasses to individualize the parsing.
    :param script: Script to be parsed
    :return: Parsed script
    """

    login_indices = [i for i, command in enumerate(script) if "docker login" in command]
    build_indices = [i for i, command in enumerate(script) if "docker build" in command]
    push_indices = [i for i, command in enumerate(script) if "docker push" in command]

    if login_indices and build_indices and push_indices:
      if login_indices[0] < build_indices[0] and build_indices[0] < push_indices[0]:
        # If the login command is before the build command, add the login command to the script
        docker_path = script[push_indices[0]].split(" ")[2]
        if ":" not in docker_path:
          docker_path += ":latest"
        image_migrated = False
        for repo in self.migrated_docker_images:
          for image in self.migrated_docker_images[repo]:
            if docker_path.endswith(image):
              image_migrated = True
              break
          if image_migrated:
            break

        if image_migrated:
          script[login_indices[
            0]] = 'echo "${{ secrets.GITHUB_TOKEN }}" | docker login ghcr.io -u "${{ github.actor }}" --password-stdin'
          build_command = script[build_indices[0]].split(" ")[4:]
          script[build_indices[
            0]] = 'docker build -t ghcr.io/$LOWERCASE_OWNER/' + repo.lower() + '/' + image.lower() + " " + " ".join(
            build_command)
          script[push_indices[0]] = 'docker push ghcr.io/$LOWERCASE_OWNER/' + repo.lower() + '/' + image.lower()
          script.insert(build_indices[0],
                        'LOWERCASE_OWNER=$(echo "${{ github.repository_owner }}" | tr "[:upper:]" "[:lower:]")')
    delete = []
    for i, command in enumerate(script):
      if "mvn" in command:
        command += (" -Dmaven.wagon.http.retryHandler.count=50 -Dmaven.wagon.http.connectionTimeout=6000000 "
                    "-Dmaven.wagon.http.readTimeout=600000000")
      # ToDo: Delete for production
      if "deploy" in command:
        delete.append(i)
        continue
      command = command.replace("${CI_JOB_TOKEN}", "${{ secrets.GITLABTOKEN }}")
      command = command.replace("$DOCKER_TOKEN", "${{ secrets.GITLABTOKEN }}")
      command = command.replace("$CI_REGISTRY_PASSWORD", "${{ secrets.GITLABTOKEN }}")
      # ToDo: Add docker, user replacement
      script[i] = command
    delete.reverse()
    for i in delete:
      script.pop(i)
    return script
