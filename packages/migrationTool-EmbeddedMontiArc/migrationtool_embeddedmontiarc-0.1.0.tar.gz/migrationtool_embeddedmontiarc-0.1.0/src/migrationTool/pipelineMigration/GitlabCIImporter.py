from typing import TextIO

import yaml

from migrationTool.pipelineMigration.Importer import Importer
from migrationTool.pipelineMigration.Job import Job
from migrationTool.pipelineMigration.Pipeline import Pipeline


class GitlabCIImporter(Importer):
  """
  Class for importing GitLab CI pipelines.
  """

  def __readStages(self) -> list[str]:
    """
    Reads the stages from the YAML data.
    :rtype: list[str]
    :return: Stages in the pipeline
    """
    return self.yaml_data['stages']

  def __readVariables(self) -> dict[str, str]:
    """
    Reads the variables from the YAML data.
    :rtype: dict[str, str]
    :return: Variables in the pipeline
    """
    return self.yaml_data.get('variables', {})

  def __flattenList(self, nested_list):
    """
    Flattens a nested list.
    :param nested_list: List with normal entries and lists
    :return: Flattened list
    """
    flattened = []
    for item in nested_list:
      if isinstance(item, list):
        flattened.extend(self.__flattenList(item))
      else:
        flattened.append(item)
    return flattened

  def __read_jobs(self) -> dict[str, Job]:
    """
    Reads the jobs from the YAML data.
    :rtype: dict[str, Job]
    :return: Jobs in the pipeline
    """
    jobs = {}
    general_image = "Ubuntu:latest"
    general_before_script = []
    if "image" in self.yaml_data:
      general_image = self.yaml_data["image"]

    if "before_script" in self.yaml_data:
      general_before_script = self.__flattenList(self.yaml_data["before_script"])

    for name, parameter in self.yaml_data.items():
      if name == "stages":
        continue
      if "script" in parameter or "trigger" in parameter:
        # Add before script in front of the normal script
        if "before_script" in parameter:
          if general_before_script:
            sc = general_before_script + self.__flattenList(parameter.get("before_script", [])) + self.__flattenList(
              parameter.get("script", []))
          else:
            sc = self.__flattenList(parameter.get("before_script", [])) + self.__flattenList(
              parameter.get("script", []))
        else:
          if general_before_script:
            sc = general_before_script + self.__flattenList(parameter.get("script", []))
          else:
            sc = self.__flattenList(parameter.get("script", []))

        # Handle dependencies
        if "dependencies" in parameter:
          needs = parameter.get("dependencies", []) + parameter.get("needs", [])
        else:
          needs = parameter.get("needs", [])
        jobs[name] = Job(name=name, image=parameter.get("image", general_image), stage=parameter.get("stage", ""),
                         script=sc, needs=needs, when=parameter.get("when", ""), exc=parameter.get("except", []),
                         artifacts=parameter.get("artifacts", []), only=parameter.get("only", []),
                         allowFailure=parameter.get("allow_failure", False), rules=parameter.get("rules", []),
                         trigger=parameter.get("trigger", {}))
    return jobs

  def __read_dependencies(self) -> tuple[dict[str, set[str]], dict[str, set[str]]]:
    """
    Reads the dependencies between jobs in the pipeline.
    :rtype: tuple[dict[str,set[str]], dict[str, set[str]]]
    :return:
    - stage_jobs: Dictionary mapping each stage to its jobs
    - job_needs: Dictionary mapping each job to its immediate dependencies
    """
    stage_jobs = {s: set() for s in self.stages}
    for jobName, jobParameter in self.jobs.items():
      stage_jobs[jobParameter.stage].add(jobName)

    job_needs = {}
    for stage in self.stages:
      for jobName in stage_jobs[stage]:
        if self.jobs[jobName].needs != []:
          for j in self.jobs[jobName].needs:
            if jobName in job_needs:
              job_needs[jobName].add(j)
            else:
              job_needs[jobName] = {j}
    return stage_jobs, job_needs

  def __get_schedule(self) -> list[str]:
    """
    Creates a schedule for the stages in the pipeline based on their dependencies and stages.
    :rtype: list[str]
    :return: List with stage names in the order of execution
    """
    stage_schedule = []
    while len(stage_schedule) != len(self.stages):
      for stage, tasks in self.stage_dependencies.items():
        if stage not in stage_schedule:
          needs_fulfilled = True
          for job in tasks:
            if job in self.needs:
              for need in self.needs[job]:
                if self.jobs[need].stage not in stage_schedule and need not in tasks:
                  needs_fulfilled = False
                  break
            if not needs_fulfilled:
              break
          else:
            stage_schedule.append(stage)
            break
    return stage_schedule

  def getPipeline(self, file: TextIO) -> Pipeline:
    """
    Imports a pipeline from a GitLab CI YAML file and returns it as a Pipeline object.
    :param file: Path to the YAML file
    :type file: TextIO
    :rtype : Pipeline
    :return: Object representing the imported pipeline
    """
    self.yaml_data = yaml.safe_load(file)
    self.stages = self.__readStages()
    self.variables = self.__readVariables()
    self.jobs = self.__read_jobs()
    self.stage_dependencies, self.needs = self.__read_dependencies()
    return Pipeline(self.stages, self.jobs, self.stage_dependencies, self.needs, self.__get_schedule(), self.variables)
