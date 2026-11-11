import logging.config
import os
from os import path

log_dir = path.join(path.dirname(path.abspath(__file__)), 'logs')
os.makedirs(log_dir, exist_ok=True)

log_file_path = path.join(
    path.dirname(path.abspath(__file__)), 'logging.ini'
)
logging.config.fileConfig(log_file_path)

pytest_plugins = [
    "src.fixtures.system.browser",
    "src.fixtures.pages",
]
