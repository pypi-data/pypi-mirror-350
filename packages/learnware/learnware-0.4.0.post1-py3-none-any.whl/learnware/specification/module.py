from typing import List, Optional, Union

import numpy as np
import pandas as pd
import torch

from datasets import Dataset

from .regular import RKMEImageSpecification, RKMETableSpecification, RKMETextSpecification, GenerativeModelSpecification
from .utils import convert_to_numpy
from ..config import C


def generate_rkme_table_spec(
    X: Union[np.ndarray, pd.DataFrame, torch.Tensor],
    gamma: float = 0.1,
    reduced_set_size: int = 100,
    step_size: float = 0.1,
    steps: int = 3,
    nonnegative_beta: bool = True,
    reduce: bool = True,
    cuda_idx: int = None,
) -> RKMETableSpecification:
    """
        Interface for users to generate Reduced Kernel Mean Embedding (RKME) specification.
        Return a RKMETableSpecification object, use .save() method to save as json file.

    Parameters
    ----------
    X : np.ndarray, pd.DataFrame, or torch.Tensor
        Raw data in np.ndarray, pd.DataFrame, or torch.Tensor format.
        The shape of X:
            First dimension represents the number of samples (data points).
            The remaining dimensions represent the dimensions (features) of each sample.
            For example, if X has shape (100, 3), it means there are 100 samples, and each sample has 3 features.
    gamma : float
        Bandwidth in gaussian kernel, by default 0.1.
    reduced_set_size : int
        Size of the construced reduced set.
    step_size : float
        Step size for gradient descent in the iterative optimization.
    steps : int
        Total rounds in the iterative optimization.
    nonnegative_beta : bool, optional
        True if weights for the reduced set are intended to be kept non-negative, by default False.
    reduce : bool, optional
        Whether shrink original data to a smaller set, by default True
    cuda_idx : int
        A flag indicating whether use CUDA during RKME computation. -1 indicates CUDA not used.
        None indicates that CUDA is automatically selected.

    Returns
    -------
    RKMETableSpecification
        A RKMETableSpecification object
    """
    # Convert data type
    X = convert_to_numpy(X)
    X = np.ascontiguousarray(X).astype(np.float32)

    # Check reduced_set_size
    max_reduced_set_size = C.max_reduced_set_size
    if reduced_set_size * X[0].size > max_reduced_set_size:
        reduced_set_size = max(20, max_reduced_set_size // X[0].size)

    # Generate rkme spec
    rkme_spec = RKMETableSpecification(gamma=gamma, cuda_idx=cuda_idx)
    rkme_spec.generate_stat_spec_from_data(X, reduced_set_size, step_size, steps, nonnegative_beta, reduce)
    return rkme_spec


def generate_rkme_image_spec(
    X: Union[np.ndarray, torch.Tensor],
    reduced_set_size: int = 50,
    step_size: float = 0.01,
    steps: int = 100,
    resize: bool = True,
    sample_size: int = 5000,
    nonnegative_beta: bool = True,
    reduce: bool = True,
    verbose: bool = True,
    cuda_idx: int = None,
    **kwargs,
) -> RKMEImageSpecification:
    """
        Interface for users to generate Reduced Kernel Mean Embedding (RKME) specification for Image.
        Return a RKMEImageSpecification object, use .save() method to save as json file.

    Parameters
    ----------
    X : np.ndarray, or torch.Tensor
        Raw data in np.ndarray, or torch.Tensor format.
        The shape of X: [N, C, H, W]
            N: Number of images.
            C: Number of channels.
            H: Height of images.
            W: Width of images.s
            For example, if X has shape (100, 3, 32, 32), it means there are 100 samples, and each sample is a 3-channel (RGB) image of size 32x32.
    reduced_set_size : int
        Size of the construced reduced set.
    step_size : float
        Step size for gradient descent in the iterative optimization.
    steps : int
        Total rounds in the iterative optimization.
    resize : bool
        Whether to scale the image to the requested size, by default True.
    nonnegative_beta : bool, optional
        True if weights for the reduced set are intended to be kept non-negative, by default False.
    reduce : bool, optional
        Whether shrink original data to a smaller set, by default True
    cuda_idx : int
        A flag indicating whether use CUDA during RKME computation. -1 indicates CUDA not used.
        None indicates that CUDA is automatically selected.
    verbose : bool, optional
        Whether to print training progress, by default True

    Returns
    -------
    RKMEImageSpecification
        A RKMEImageSpecification object
    """

    # Generate rkme spec
    rkme_image_spec = RKMEImageSpecification(cuda_idx=cuda_idx)
    rkme_image_spec.generate_stat_spec_from_data(
        X, reduced_set_size, step_size, steps, resize, sample_size, nonnegative_beta, reduce, verbose, **kwargs
    )
    return rkme_image_spec


def generate_rkme_text_spec(
    X: List[str],
    gamma: float = 0.1,
    reduced_set_size: int = 100,
    step_size: float = 0.1,
    steps: int = 3,
    nonnegative_beta: bool = True,
    reduce: bool = True,
    cuda_idx: int = None,
) -> RKMETextSpecification:
    """
        Interface for users to generate Reduced Kernel Mean Embedding (RKME) specification for Text.
        Return a RKMETextSpecification object, use .save() method to save as json file.

    Parameters
    ----------
    X : List[str]
        Raw data of text.
    gamma : float
        Bandwidth in gaussian kernel, by default 0.1.
    reduced_set_size : int
        Size of the construced reduced set.
    step_size : float
        Step size for gradient descent in the iterative optimization.
    steps : int
        Total rounds in the iterative optimization.
    nonnegative_beta : bool, optional
        True if weights for the reduced set are intended to be kept non-negative, by default False.
    reduce : bool, optional
        Whether shrink original data to a smaller set, by default True
    cuda_idx : int
        A flag indicating whether use CUDA during RKME computation. -1 indicates CUDA not used.
        None indicates that CUDA is automatically selected.

    Returns
    -------
    RKMETextSpecification
        A RKMETextSpecification object
    """
    # Check input type
    if not isinstance(X, list) or not all(isinstance(item, str) for item in X):
        raise TypeError("Input data must be a list of strings.")

    # Generate rkme text spec
    rkme_text_spec = RKMETextSpecification(gamma=gamma, cuda_idx=cuda_idx)
    rkme_text_spec.generate_stat_spec_from_data(X, reduced_set_size, step_size, steps, nonnegative_beta, reduce)
    return rkme_text_spec


def generate_generative_model_spec(
    dataset: Optional[Dataset] = None,
    dataset_text_field="text",
    X: List[str] = None,
    verbose: bool = True,
    **kwargs   
) -> GenerativeModelSpecification:
    # Check input type
    if X is not None and (not isinstance(X, list) or not all(isinstance(item, str) for item in X)):
        raise TypeError("Input data must be a list of strings.")
    
    # Generate generative model spec
    task_vector_spec = GenerativeModelSpecification()
    task_vector_spec.generate_stat_spec_from_data(dataset=dataset, dataset_text_field=dataset_text_field, X=X, verbose=verbose, **kwargs)
    
    return task_vector_spec


def generate_stat_spec(
    type: str, X: Union[np.ndarray, pd.DataFrame, torch.Tensor, List[str]], *args, **kwargs
) -> Union[RKMETableSpecification, RKMEImageSpecification, RKMETextSpecification]:
    """
        Interface for users to generate statistical specification.
        Return a StatSpecification object, use .save() method to save as npy file.

    Parameters
    ----------
    type: str
        Type of statistical specification.
        Supported types: "table", "text", "image"
    X : np.ndarray
        Raw data in np.ndarray format.
        Size of array: (n*d)

    Returns
    -------
    StatSpecification
        A StatSpecification object
    """
    if type == "table":
        return generate_rkme_table_spec(X=X, *args, **kwargs)
    elif type == "text":
        return generate_rkme_text_spec(X=X, *args, **kwargs)
    elif type == "image":
        return generate_rkme_image_spec(X=X, *args, **kwargs)
    else:
        raise TypeError(f"type {type} is not supported!")


def generate_semantic_spec(
    name: Optional[str] = None,
    description: Optional[str] = None,
    data_type: Optional[str] = None,
    task_type: Optional[str] = None,
    model_type: Optional[str] = None,
    library_type: Optional[str] = None,
    scenarios: Optional[Union[str, List[str]]] = None,
    license: Optional[Union[str, List[str]]] = None,
    input_description: Optional[dict] = None,
    output_description: Optional[dict] = None,
):
    semantic_specification = dict()
    semantic_specification["Data"] = {"Type": "Class", "Values": [data_type] if data_type is not None else []}
    semantic_specification["Task"] = {"Type": "Class", "Values": [task_type] if task_type is not None else []}
    semantic_specification["Model"] = {"Type": "Optional", "Values": [model_type] if model_type is not None else ["Others"]}
    semantic_specification["Library"] = {
        "Type": "Class",
        "Values": [library_type] if library_type is not None else [],
    }

    license = [license] if isinstance(license, str) else license
    semantic_specification["License"] = {"Type": "Class", "Values": license if license is not None else []}
    scenarios = [scenarios] if isinstance(scenarios, str) else scenarios
    semantic_specification["Scenario"] = {"Type": "Tag", "Values": scenarios if scenarios is not None else []}

    semantic_specification["Name"] = {"Type": "String", "Values": name if name is not None else ""}
    semantic_specification["Description"] = {
        "Type": "String",
        "Values": description if description is not None else "",
    }
    if input_description is not None:
        semantic_specification["Input"] = input_description

    if output_description is not None:
        semantic_specification["Output"] = output_description

    return semantic_specification
