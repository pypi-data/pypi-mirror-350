import os
import re

# Pattern for env variaboles in maven
env_var_pattern = re.compile(r"\$\{env\.(\w+)\}")


def find_env_vars_in_file(file_path):
  """
  Find environment variables in a given file.
  :param file_path: Path to file
  :return: set - Set of environment variables found in the file
  """
  env_vars = set()
  with open(file_path, "r", errors="ignore") as file:
    content = file.read()
    matches = env_var_pattern.findall(content)
    env_vars.update(matches)
  return env_vars


def find_env_vars_in_repo(repo_path):
  """
  Find environment variables in all XML files in a given repository.
  :param repo_path: Path to the repository
  :return: set - Set of environment variables found in the repository
  """
  envVars = set()
  for root, _, files in os.walk(repo_path):
    for file in files:
      if file.endswith(".xml"):
        file_path = os.path.join(root, file)
        found = find_env_vars_in_file(file_path)
        if found:
          envVars.update(found)
  return envVars


if __name__ == "__main__":
  repos = ["../repos/EMADL2CPP", "../repos/MNISTCalculator"]
  for repo_path in repos:
    # repo_path = '../repos/EMADL2CPP'  # Path to the git repository
    print(repo_path)
    env_vars = find_env_vars_in_repo(repo_path)
    env_All = set()
    for file_path, env_vars in env_vars.items():
      print(f"Environment variables found in {file_path}:")
      for env_var in env_vars:
        print(f"  {env_var}")
      env_All.update(env_vars)
    print("--------------------------")
    print(env_All)
