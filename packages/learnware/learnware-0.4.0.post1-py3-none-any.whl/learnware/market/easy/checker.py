import random
import string
import traceback

import numpy as np
import torch

from ..base import BaseChecker
from ..utils import parse_specification_type
from ...config import C
from ...logger import get_module_logger
from ...specification import LLMGeneralCapabilitySpecification
from ...specification.system.llm_general_capability_spec.config import test_benchmark_configs

logger = get_module_logger("easy_checker", "INFO")


class EasySemanticChecker(BaseChecker):
    @staticmethod
    def check_semantic_spec(semantic_spec):
        try:
            for key in C["semantic_specs"]:
                if C["semantic_specs"][key]["Type"] == "Optional":
                    if key not in semantic_spec:
                        continue
                    pass

                value = semantic_spec[key]["Values"]
                valid_type = C["semantic_specs"][key]["Type"]
                assert semantic_spec[key]["Type"] == valid_type, f"{key} type mismatch"

                if valid_type == "Class" or valid_type == "Optional":
                    valid_list = C["semantic_specs"][key]["Values"]
                    assert len(value) == 1, f"{key} must be unique"
                    assert value[0] in valid_list, f"{key} must be in {valid_list}"

                elif valid_type == "Tag":
                    valid_list = C["semantic_specs"][key]["Values"]
                    assert len(value) >= 1, f"{key} cannot be empty"
                    for v in value:
                        assert v in valid_list, f"{key} must be in {valid_list}"

                elif valid_type == "String":
                    assert isinstance(value, str), f"{key} must be string"
                    assert len(value) >= 1, f"{key} cannot be empty"

            if semantic_spec["Data"]["Values"][0] == "Table":
                assert semantic_spec["Input"] is not None, "Lack of input semantics"
                dim = semantic_spec["Input"]["Dimension"]
                for k, v in semantic_spec["Input"]["Description"].items():
                    assert int(k) >= 0 and int(k) < dim, f"Dimension number in [0, {dim})"
                    assert isinstance(v, str), "Description must be string"

                assert semantic_spec["Task"]["Values"][0] in [
                    "Classification",
                    "Regression",
                    "Feature Extraction",
                    "Others",
                ]

                assert semantic_spec["Model"]["Values"][0] == "Others"

            if semantic_spec["Data"]["Values"][0] == "Image":
                assert semantic_spec["Task"]["Values"][0] in [
                    "Classification",
                    "Regression",
                    "Feature Extraction",
                    "Segmentation",
                    "Object Detection",
                    "Others",
                ]

                assert semantic_spec["Model"]["Values"][0] == "Others"

            if semantic_spec["Data"]["Values"][0] == "Text":
                assert semantic_spec["Task"]["Values"][0] in [
                    "Classification",
                    "Regression",
                    "Feature Extraction",
                    "Text Generation",
                    "Others",
                ]

            if semantic_spec["Task"]["Values"][0] in ["Classification", "Regression"]:
                assert semantic_spec["Output"] is not None, "Lack of output semantics"
                dim = semantic_spec["Output"]["Dimension"]
                assert (
                    dim > 1 or semantic_spec["Task"]["Values"][0] == "Regression"
                ), "Classification task must have dimension > 1"

                for k, v in semantic_spec["Output"]["Description"].items():
                    assert int(k) >= 0 and int(k) < dim, f"Dimension number in [0, {dim})"
                    assert isinstance(v, str), "Description must be string"

            return EasySemanticChecker.NONUSABLE_LEARNWARE, "EasySemanticChecker Success"

        except Exception as err:
            logger.warning(f"semantic_specification is not valid due to {err}!")
            return EasySemanticChecker.INVALID_LEARNWARE, traceback.format_exc()

    def __call__(self, learnware):
        semantic_spec = learnware.get_specification().get_semantic_spec()
        return self.check_semantic_spec(semantic_spec)


class EasyStatChecker(BaseChecker):
    @staticmethod
    def _generate_random_text_list(num, text_type="en", min_len=10, max_len=1000):
        text_list = []
        for i in range(num):
            length = random.randint(min_len, max_len)
            if text_type == "en":
                characters = string.ascii_letters + string.digits + string.punctuation
                result_str = "".join(random.choice(characters) for i in range(length))
                text_list.append(result_str)
            elif text_type == "zh":
                result_str = "".join(chr(random.randint(0x4E00, 0x9FFF)) for i in range(length))
                text_list.append(result_str)
            else:
                raise ValueError("Type should be en or zh")
        return text_list

    def __call__(self, learnware):
        semantic_spec = learnware.get_specification().get_semantic_spec()

        try:
            # Check model instantiation
            learnware.instantiate_model()

        except Exception as e:
            traceback.print_exc()
            logger.warning(f"The learnware [{learnware.id}] is instantiated failed! Due to {e}.")
            return self.INVALID_LEARNWARE, traceback.format_exc()
        try:
            # Check input shape
            learnware_model = learnware.get_model()
            input_shape = learnware_model.input_shape

            if semantic_spec["Data"]["Values"][0] == "Table" and input_shape != (
                int(semantic_spec["Input"]["Dimension"]),
            ):
                message = "input shapes of model and semantic specifications are different"
                logger.warning(message)
                return self.INVALID_LEARNWARE, message

            # check llm base model learnware general capability
            if (
                semantic_spec["Data"]["Values"] == ["Text"]
                and semantic_spec["Task"]["Values"] == ["Text Generation"]
                and semantic_spec["Model"]["Values"] == ["Base Model"]
            ):
                try:
                    general_capability_spec = LLMGeneralCapabilitySpecification()
                    general_capability_spec.generate_stat_spec_from_system(
                        learnware=learnware, benchmark_configs=test_benchmark_configs
                    )
                    learnware.update_stat_spec(general_capability_spec.type, general_capability_spec)
                except Exception:
                    message = (
                        f"The learnware [{learnware.id}] llm base model general capability evaluation is not available!"
                    )
                    logger.warning(message)
                    message += "\r\n" + traceback.format_exc()
                    return self.INVALID_LEARNWARE, message

            # Check statistical specification
            spec_type = parse_specification_type(learnware.get_specification().stat_spec)
            if spec_type is None:
                message = f"No valid specification is found in stat spec {spec_type}"
                logger.warning(message)
                return self.INVALID_LEARNWARE, message

            # Check if statistical specification is computable in dist()
            if spec_type != "LLMGeneralCapabilitySpecification":
                stat_spec = learnware.get_specification().get_stat_spec_by_name(spec_type)
                distance = float(stat_spec.dist(stat_spec))
                if not np.isfinite(distance):
                    message = f"The distance between statistical specifications is not finite, where distance={distance}"
                    logger.warning(message)
                    return self.INVALID_LEARNWARE, message

            if spec_type == "RKMETableSpecification":
                if not isinstance(input_shape, tuple) or not all(isinstance(item, int) for item in input_shape):
                    raise ValueError(
                        f"For RKMETableSpecification, input_shape should be tuple of int, but got {input_shape}"
                    )

                if stat_spec.get_z().shape[1:] != input_shape:
                    message = f"The learnware [{learnware.id}] input dimension mismatch with stat specification."
                    logger.warning(message)
                    return self.INVALID_LEARNWARE, message
                inputs = np.random.randn(10, *input_shape)

            elif spec_type in ["RKMETextSpecification", "GenerativeModelSpecification", "LLMGeneralCapabilitySpecification"]:

                if semantic_spec["Model"]["Values"][0] != "Others":
                    len_ = random.randint(10, 1000)
                    inputs = EasyStatChecker._generate_random_text_list(10, "en", len_, len_)
                else:
                    inputs = EasyStatChecker._generate_random_text_list(10)

            elif spec_type == "RKMEImageSpecification":
                if not isinstance(input_shape, tuple) or not all(isinstance(item, int) for item in input_shape):
                    raise ValueError(
                        f"For RKMEImageSpecification, input_shape should be tuple of int, but got {input_shape}"
                    )
                inputs = np.random.randint(0, 255, size=(10, *input_shape))

            else:
                raise ValueError(f"not supported spec type for spec_type = {spec_type}")

            # Check output
            try:
                outputs = learnware.predict(inputs)
            except Exception:
                message = f"The learnware [{learnware.id}] prediction is not available!"
                logger.warning(message)
                message += "\r\n" + traceback.format_exc()
                return self.INVALID_LEARNWARE, message

            # Check length of input and output
            if len(inputs) != len(outputs):
                message = f"The learnware [{learnware.id}] output length must be equal to input length!"
                logger.warning(message)
                return self.INVALID_LEARNWARE, message

            if learnware_model.output_shape is not None or semantic_spec["Task"]["Values"][0] in [
                "Classification",
                "Regression",
                "Feature Extraction",
            ]:
                # Check output type
                if isinstance(outputs, torch.Tensor):
                    outputs = outputs.detach().cpu().numpy()
                if not isinstance(outputs, np.ndarray):
                    message = f"The learnware [{learnware.id}] output must be np.ndarray or torch.Tensor!"
                    logger.warning(message)
                    return self.INVALID_LEARNWARE, message

                if outputs.ndim == 1:
                    outputs = outputs.reshape(-1, 1)

                # Check output shape
                if outputs[0].shape != learnware_model.output_shape:
                    message = f"The learnware [{learnware.id}] output dimension mismatch, where pred_shape={outputs[0].shape}, model_shape={learnware_model.output_shape}"
                    logger.warning(message)
                    return self.INVALID_LEARNWARE, message

                # Check output dimension for regression
                if semantic_spec["Task"]["Values"][0] == "Regression" and learnware_model.output_shape[0] != int(
                    semantic_spec["Output"]["Dimension"]
                ):
                    message = f"The learnware [{learnware.id}] output dimension mismatch, where model_shape={learnware_model.output_shape}, semantic_shape={(int(semantic_spec['Output']['Dimension']), )}"
                    logger.warning(message)
                    return self.INVALID_LEARNWARE, message

                # Check output dimension for classification
                if semantic_spec["Task"]["Values"][0] == "Classification":
                    model_output_shape = learnware_model.output_shape[0]
                    semantic_output_shape = int(semantic_spec["Output"]["Dimension"])

                    if model_output_shape == 1:
                        if isinstance(outputs, torch.Tensor):
                            outputs = outputs.detach().cpu().numpy()
                        if isinstance(outputs, list):
                            outputs = np.array(outputs)

                        if not np.all(np.logical_and(outputs >= 0, outputs < semantic_output_shape)):
                            message = f"The learnware [{learnware.id}] output label mismatch, where outputs of model is {outputs}, semantic_shape={(semantic_output_shape, )}"
                            logger.warning(message)
                            return self.INVALID_LEARNWARE, message
                    else:
                        if model_output_shape != semantic_output_shape:
                            message = f"The learnware [{learnware.id}] output dimension mismatch, where model_shape={learnware_model.output_shape}, semantic_shape={(semantic_output_shape, )}"
                            logger.warning(message)
                            return self.INVALID_LEARNWARE, message

        except Exception as e:
            message = f"The learnware [{learnware.id}] is not valid! Due to {repr(e)}."
            logger.warning(message)
            return self.INVALID_LEARNWARE, message

        return self.USABLE_LEARNWARE, "EasyStatChecker Success"
