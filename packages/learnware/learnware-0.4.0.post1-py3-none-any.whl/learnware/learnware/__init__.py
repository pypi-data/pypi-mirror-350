import copy
import os
import traceback
from typing import Optional

from .base import Learnware
from .utils import get_stat_spec_from_config
from ..config import C
from ..logger import get_module_logger
from ..specification import Specification
from ..utils import read_yaml_to_dict

logger = get_module_logger("learnware.learnware")


def get_learnware_from_dirpath(
    id: str, semantic_spec: dict, learnware_dirpath, ignore_error=True
) -> Optional[Learnware]:
    """Get the learnware object from dirpath, and provide the manage interface tor Learnware class

    Parameters
    ----------
    id : str
        The learnware id that is given by learnware market
    semantic_spec : dict
        The learnware semantice specifactions
    learnware_dirpath : str
        The dirpath of learnware folder

    Returns
    -------
    Learnware
        The contructed learnware object, return None if build failed
    """
    learnware_config = {
        "model": {
            "class_name": "Model",
            "weights_file_path": "weights",
            "required_learnware_ids": [],
            "kwargs": {},
        },
        "stat_specifications": [],
    }

    try:
        learnware_yaml_path = os.path.join(learnware_dirpath, C.learnware_folder_config["yaml_file"])
        assert os.path.exists(
            learnware_yaml_path
        ), f"learnware.yaml is not found for learnware_{id}, please check the learnware folder or zipfile."

        yaml_config = read_yaml_to_dict(learnware_yaml_path)

        if "name" in yaml_config:
            learnware_config["name"] = yaml_config["name"]
        if "model" in yaml_config:
            learnware_config["model"].update(yaml_config["model"])
        if "stat_specifications" in yaml_config:
            learnware_config["stat_specifications"] = yaml_config["stat_specifications"].copy()

        if "module_path" not in learnware_config["model"]:
            learnware_config["model"]["module_path"] = C.learnware_folder_config["module_file"]

        if (
            semantic_spec["Data"]["Values"] == ["Text"]
            and semantic_spec["Task"]["Values"] == ["Text Generation"]
        ):
            if "weights_file_path" not in learnware_config["model"]:
                learnware_config["model"]["weights_file_path"] = C.learnware_folder_config["weights_file_path"]
                
            learnware_weights_path = os.path.join(learnware_dirpath, learnware_config["model"]["weights_file_path"])
            assert os.path.exists(
                learnware_weights_path
            ), f"Weights are not found for the Text Generation Model learnware_{id}, please check the learnware.yaml or zipfile."
            
            if semantic_spec["Model"]["Values"] == ["PEFT Model"]:
                assert "required_learnware_ids" in learnware_config["model"], f"'required_learnware_ids' is not found for the PEFT Model learnware_{id}, please check the learnware.yaml."
                assert len(learnware_config["model"]["required_learnware_ids"]) != 0, f"'required_learnware_ids' can't be empty for the PEFT Model learnware_{id}, please check the learnware.yaml."           

        learnware_spec = Specification()
        for _stat_spec in learnware_config["stat_specifications"]:
            stat_spec = _stat_spec.copy()
            stat_spec_path = os.path.join(learnware_dirpath, stat_spec["file_name"])
            assert os.path.exists(
                stat_spec_path
            ), f"statistical specification file {stat_spec['file_name']} is not found for learnware_{id}, please check the learnware folder or zipfile."

            stat_spec["file_name"] = stat_spec_path
            stat_spec_inst = get_stat_spec_from_config(stat_spec)
            learnware_spec.update_stat_spec(**{stat_spec_inst.type: stat_spec_inst})

        learnware_spec.update_semantic_spec(copy.deepcopy(semantic_spec))

    except Exception as e:
        if not ignore_error:
            raise e
        logger.warning(f"Load Learnware {id} failed! Due to {e}; details:\n{traceback.format_exc()}")
        return None

    return Learnware(
        id=id, model=learnware_config["model"], specification=learnware_spec, learnware_dirpath=learnware_dirpath
    )
