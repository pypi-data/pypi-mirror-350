from .base import BaseStatSpecification, Specification
from .regular import (
    RegularStatSpecification,
    RKMEImageSpecification,
    RKMEStatSpecification,
    RKMETableSpecification,
    RKMETextSpecification,
    GenerativeModelSpecification,
    rkme_solve_qp,
)
from .system import HeteroMapTableSpecification, LLMGeneralCapabilitySpecification
from ..utils import is_torch_available

if not is_torch_available(verbose=False):
    generate_stat_spec = None
    generate_rkme_table_spec = None
    generate_rkme_image_spec = None
    generate_rkme_text_spec = None
    generate_generative_model_spec = None
    generate_semantic_spec = None
else:
    from .module import (
        generate_rkme_image_spec,
        generate_rkme_table_spec,
        generate_rkme_text_spec,
        generate_generative_model_spec,
        generate_semantic_spec,
        generate_stat_spec,
    )

__all__ = [
    "BaseStatSpecification",
    "Specification",
    "RegularStatSpecification",
    "RKMEImageSpecification",
    "RKMEStatSpecification",
    "RKMETableSpecification",
    "RKMETextSpecification",
    "GenerativeModelSpecification",
    "HeteroMapTableSpecification",
    "LLMGeneralCapabilitySpecification",
    "rkme_solve_qp",
    "generate_rkme_image_spec",
    "generate_rkme_table_spec",
    "generate_rkme_text_spec",
    "generate_generative_model_spec",
    "generate_semantic_spec",
    "generate_stat_spec",
]
