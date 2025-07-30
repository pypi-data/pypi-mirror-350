import importlib.metadata
from typing import Dict


def get_package_info(package_name: str) -> Dict:
    try:
        metadata = importlib.metadata.metadata(package_name)
        return metadata.json
    except importlib.metadata.PackageNotFoundError as e:
        raise e


def package_exists(package_name: str) -> bool:
    try:
        __import__(package_name)
        return True
    except ImportError:
        return False
