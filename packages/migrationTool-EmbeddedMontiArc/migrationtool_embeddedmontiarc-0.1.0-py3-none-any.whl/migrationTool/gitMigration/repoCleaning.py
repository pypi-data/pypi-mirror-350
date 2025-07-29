import os
import subprocess

import git


def split_large_files2(directory, size="90M"):
  """To be removed"""
  try:
    command = f'find {directory} -type f -size +{size} -exec sh -c \'split -b {size} "$0" "$0.part"\' {{}} \\;'
    result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
    print("Split command output:", result.stdout.decode())
  except subprocess.CalledProcessError as e:
    print("Error:", e.stderr.decode(errors="replace"))
  repo = git.Repo(directory)
  repo.git.add(all=True)
  repo.index.commit("Split large files into smaller parts")


def split_large_files(directory, size="90M", output=False):
  """
      Splits files in the repository greater than size into parts. The changes are then committed. Works only on Linux.
  :param directory: Directory of the repository
  :param size: Size of the files to be split
  """
  # ToDo: Rewrite for windows, very low priority
  try:
    # command = f"find {directory} -type f -size +{size} -exec sh -c 'split -b {size} --suffix-length=1 \"$0\"
    # \"$0.part\"' {{}} \\;"
    command = (f'find {directory} -path {directory}/.git -prune -o -type f -size +{size} -exec sh -c \'split -b {size} '
               f'--suffix-length=1 "$0" "$0.part"\' {{}} \\;')
    result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
    if output:
      print(result.stdout.decode())
    """
# Prints all files that have been split
find_command = f"find {directory} -path {directory}/.git -prune -o -type f -size +{size} -print"
find_result = subprocess.run(find_command, shell=True, check=True, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
files = find_result.stdout.decode().strip().split("\n")
print("Files that have been split:")
for file in files:
    print(f" - {file}")
"""
  except subprocess.CalledProcessError as e:
    print("Error:", e.stderr.decode(errors="replace"))
  repo = git.Repo(directory)
  repo.git.add(all=True)
  repo.index.commit("Split large files into smaller parts")


def remove_lfs(directory):
  """
      Removes LFS from the repository and migrates the files to normal git objects.
  :param directory: Directory of the repository
  """
  repo = git.Repo(directory)
  repo.git.lfs("migrate", "export", "--everything", "--include", "*")
  repo.git.lfs("uninstall")


def remove_lfs_from_gitattributes(directory):
  """
      Removes LFS from all .gitattributes files in the repository.
  :param directory: Directory of the repository
  """
  changes = False
  for root, _, files in os.walk(directory):
    for file in files:
      if file == ".gitattributes":
        file_path = os.path.join(root, file)
        with open(file_path, "r") as f:
          lines = f.readlines()
        with open(file_path, "w") as f:
          for line in lines:
            if "filter=lfs" not in line:
              f.write(line)
        changes = True
  if changes:
    repo = git.Repo(directory)
    repo.git.add(all=True)
    repo.index.commit("Removed LFS from .gitattributes")


def concatenate_files(directory):
  """
      ONLY FOR DEBUGGING.Concatenates all .part files in the directory and removes the original .part files.
  :param directory: Directory of the repository
  """
  try:
    command = (f'find {directory} -type f -name \'*.part*\' | while read part; do base=$(echo "$part" | sed '
               f'\'s/.part.*//\'); cat "$part" >> "$base"; rm "$part"; done')
    result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
    print("Concatenate command output:", result.stdout.decode())
  except subprocess.CalledProcessError as e:
    print("Error:", e.stderr.decode(errors="replace"))


if __name__ == "__main__":
  # run_git_filter_repo()
  split_large_files("../repos/MNISTCalculator")  # concatenate_files("./test")
