from .organizer import EasyOrganizer
from ...logger import get_module_logger
from ...utils import is_torch_available

logger = get_module_logger("market_easy")

if not is_torch_available(verbose=False):
    EasySemanticChecker = None
    EasyStatChecker = None
    EasyExactSemanticSearcher = None
    EasyFuzzSemanticSearcher = None
    EasyStatSearcher = None
    SeqCombinedSearcher = None
    logger.error("EasySeacher and EasyChecker are not available because 'torch' is not installed!")
else:
    from .checker import EasySemanticChecker, EasyStatChecker
    from .searcher import EasyExactSemanticSearcher, EasyFuzzSemanticSearcher, EasyStatSearcher, SeqCombinedSearcher

__all__ = [
    "EasyOrganizer",
    "EasySemanticChecker",
    "EasyStatChecker",
    "EasyExactSemanticSearcher",
    "EasyFuzzSemanticSearcher",
    "EasyStatSearcher",
    "SeqCombinedSearcher",
]
