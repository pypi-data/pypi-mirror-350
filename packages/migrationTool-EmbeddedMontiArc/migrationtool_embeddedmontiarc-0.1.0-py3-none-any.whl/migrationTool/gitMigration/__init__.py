import logging

from .Git import Git
from .GithubUploader import GithubUploader
from .GitlabDownloader import GitlabDownloader
from .largeFiles import run_git_filter_repo
from .repoCleaning import remove_lfs, split_large_files, remove_lfs_from_gitattributes

# Entferne alle Handler des Root-Loggers
root_logger = logging.getLogger()
for handler in root_logger.handlers[:]:
  root_logger.removeHandler(handler)

# Füge einen FileHandler zum Root-Logger hinzu
file_handler = logging.FileHandler("output.log")
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", datefmt='%H:%M:%S'))
root_logger.addHandler(file_handler)

# Setze das Logging-Level des Root-Loggers
root_logger.setLevel(logging.INFO)

# Beispiel für einen spezifischen Logger
logger = logging.getLogger(__name__)
