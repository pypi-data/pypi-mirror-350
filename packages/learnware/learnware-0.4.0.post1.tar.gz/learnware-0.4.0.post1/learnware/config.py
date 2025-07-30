import copy
import logging
import os
from enum import Enum


class Config:
    def __init__(self, default_conf):
        self.__dict__["_default_config"] = copy.deepcopy(default_conf)  # avoiding conflictions with __getattr__
        self.reset()

    def __getitem__(self, key):
        return self.__dict__["_config"][key]

    def __getattr__(self, attr):
        if attr in self.__dict__["_config"]:
            return self.__dict__["_config"][attr]

        raise AttributeError(f"No such {attr} in self._config")

    def get(self, key, default=None):
        return self.__dict__["_config"].get(key, default)

    def __setitem__(self, key, value):
        self.__dict__["_config"][key] = value

    def __setattr__(self, attr, value):
        self.__dict__["_config"][attr] = value

    def __contains__(self, item):
        return item in self.__dict__["_config"]

    def __getstate__(self):
        return self.__dict__

    def __setstate__(self, state):
        self.__dict__.update(state)

    def __str__(self):
        return str(self.__dict__["_config"])

    def __repr__(self):
        return str(self.__dict__["_config"])

    def reset(self):
        self.__dict__["_config"] = copy.deepcopy(self._default_config)

    def update(self, *args, **kwargs):
        self.__dict__["_config"].update(*args, **kwargs)


class SystemType(Enum):
    LINUX = 0
    MACOS = 1
    WINDOWS = 2


def get_platform():
    import platform

    os_name = platform.system().lower()
    if "macos" in os_name or "darwin" in os_name:
        return SystemType.MACOS
    elif "windows" in os_name:
        return SystemType.WINDOWS
    elif "linux" in os_name:
        return SystemType.LINUX
    raise SystemError("Learnware only support MACOS/Linux/Windows")


if get_platform() == SystemType.MACOS:
    ROOT_DIRPATH = os.path.join(os.path.expanduser("~"), "Library", "Learnware")
else:
    ROOT_DIRPATH = os.path.join(os.path.expanduser("~"), ".learnware")

PACKAGE_DIRPATH = os.path.dirname(os.path.abspath(__file__))

DATABASE_PATH = os.path.join(ROOT_DIRPATH, "database")
STDOUT_PATH = os.path.join(ROOT_DIRPATH, "stdout")
CACHE_PATH = os.path.join(ROOT_DIRPATH, "cache")


semantic_config = {
    "Data": {
        "Values": ["Table", "Image", "Text"],
        "Type": "Class",
    },  # Choose only one class
    "Task": {
        "Values": [
            "Classification",
            "Regression",
            "Feature Extraction",
            "Segmentation",
            "Object Detection",
            "Text Generation",
            "Others",
        ],
        "Type": "Class",  # Choose only one class
    },
    "Model": {
        "Values": [
            "Base Model",
            "Fine-tuned Model",
            "PEFT Model",
            "Others",
        ],
        "Type": "Optional",
    },
    "Library": {
        "Values": ["Scikit-learn", "PyTorch", "TensorFlow", "Others"],
        "Type": "Class",
    },  # Choose one or more tags
    "Scenario": {
        "Values": [
            "Business",
            "Financial",
            "Health",
            "Politics",
            "Computer",
            "Internet",
            "Traffic",
            "Nature",
            "Fashion",
            "Industry",
            "Agriculture",
            "Education",
            "Entertainment",
            "Architecture",
            "Others",
        ],
        "Type": "Tag",  # Choose one or more tags
    },
    "Description": {
        "Values": None,
        "Type": "String",
    },
    "Name": {
        "Values": None,
        "Type": "String",
    },
    "License": {
        "Values": [
            "MIT",
            "Apache-2.0",
            "BSD-2-Clause",
            "BSD-3-Clause",
            "GPL-2.0",
            "GPL-3.0",
            "LGPL-2.1",
            "LGPL-3.0",
            "AGPL-3.0",
            "ECL-2.0",
            "AFL-3.0",
            "CC-BY-4.0",
            "CC-BY-SA-4.0",
            "Others",
        ],
        "Type": "Class",
    },
}

_DEFAULT_CONFIG = {
    "root_path": ROOT_DIRPATH,
    "package_path": PACKAGE_DIRPATH,
    "database_path": DATABASE_PATH,
    "stdout_path": STDOUT_PATH,
    "cache_path": CACHE_PATH,
    "logging_level": logging.INFO,
    "logging_outfile": None,
    "semantic_specs": semantic_config,
    "market_root_path": ROOT_DIRPATH,
    "learnware_folder_config": {
        "yaml_file": "learnware.yaml",
        "module_file": "__init__.py",
        "weights_file_path" : "weights",
    },
    "database_url": f"sqlite:///{DATABASE_PATH}",
    "max_reduced_set_size": 1310720,
    "backend_host": "https://bmwu.cloud/api",
    "random_seed": 0,
}

C = Config(_DEFAULT_CONFIG)
