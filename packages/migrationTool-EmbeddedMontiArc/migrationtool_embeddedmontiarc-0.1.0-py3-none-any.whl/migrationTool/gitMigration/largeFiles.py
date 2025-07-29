import os
import subprocess

from tqdm import tqdm

# Define size limit (100MB)
SIZE_LIMIT = 100 * 1024 * 1024  # 100MB in bytes


def get_git_root(repo_path):
  """
  Check if the provided path is a Git repository and return its root.
  :param repo_path: Path to the repository
  :return: Path to the root of the Git repository or None if not a Git repository.
  """
  try:
    root = (subprocess.check_output(["git", "-C", repo_path, "rev-parse", "--show-toplevel"]).strip().decode())
    return root
  except subprocess.CalledProcessError:
    return None


def run_git_filter_repo(path=".", size="100M", output=False):
  """
      Runs the git filter-repo command to remove large files from the git history.
  :param path: path to the repository
  :param size: size of the files to be filtered must end with M
  :return:
  """
  try:
    result = subprocess.run(["git", "filter-repo", "--strip-blobs-bigger-than", size, "--force"], check=True,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=path, )
    if output:
      print("Git filter repo output:", result.stdout.decode())
  except subprocess.CalledProcessError as e:
    print("Error:", e.stderr.decode(errors="replace"))


def find_large_files_in_repo(repo_path):
  """
  Find large files in the working directory (latest commit).
  :param repo_path: Path to the repository
  """

  print("\nScanning for large files in the current working directory...")
  try:
    result = subprocess.check_output(["git", "-C", repo_path, "ls-files", "-s"]).decode()
    for line in result.splitlines():
      parts = line.split()
      if len(parts) >= 4:
        file_path = os.path.join(repo_path, parts[3])
        if os.path.exists(file_path):
          size = os.path.getsize(file_path)
          if size > SIZE_LIMIT:
            print(f"Large file found: {file_path} ({size / (1024 * 1024):.2f} MB)")
  except subprocess.CalledProcessError as e:
    print(f"Error: {e}")


def findLargeFilesInHistory(repo_path):
  """Find large files in the Git commit history."""
  try:
    # Get all blob objects in the repo history
    blobs = subprocess.check_output(["git", "-C", repo_path, "rev-list", "--objects", "--all"]).decode()
    blob_lines = blobs.splitlines()

    output = ""
    for line in tqdm(blob_lines, desc="Scanning history"):
      parts = line.split()
      if len(parts) == 2:
        blob_hash, file_path = parts
        # Get the file size
        size_output = (subprocess.check_output(["git", "-C", repo_path, "cat-file", "-s", blob_hash]).decode().strip())
        size = int(size_output)
        if size > SIZE_LIMIT:
          output += f"   -  {file_path} ({size / (1024 * 1024):.2f} MB)\n"
    if output:
      print("Large files found in history:")
      print(output)
    else:
      print("No large files found in history.")
  except subprocess.CalledProcessError as e:
    print(f"Error: {e}")


if __name__ == "__main__":
  repo_path = "../../repos/MNISTCalculator"

  # Validate the repository
  repo_root = get_git_root(repo_path)
  if repo_root:
    print(f"Git Repository: {repo_root}")
    find_large_files_in_repo(repo_root)
    findLargeFilesInHistory(repo_root)
