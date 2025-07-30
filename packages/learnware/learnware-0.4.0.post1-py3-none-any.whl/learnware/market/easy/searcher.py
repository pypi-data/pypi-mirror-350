import math
from typing import List, Optional, Tuple, Union

import numpy as np
import torch
from rapidfuzz import fuzz

from ..base import (
    BaseOrganizer,
    BaseSearcher,
    AtomicSearcher,
    BaseUserInfo,
    MultipleSearchItem,
    SearchResults,
    SingleSearchItem,
)
from ..utils import parse_specification_type
from ...learnware import Learnware
from ...logger import get_module_logger
from ...specification import RKMEImageSpecification, RKMETableSpecification, RKMETextSpecification, rkme_solve_qp

logger = get_module_logger("easy_seacher")


class EasyExactSemanticSearcher(AtomicSearcher):
    def is_applicable_learnware(self, learnware: Learnware) -> bool:
        return True

    def is_applicable_user(self, user_info: BaseUserInfo) -> bool:
        return True

    def _learnware_id_search(self, learnware_id: str, learnware_list: List[Learnware]) -> List[Learnware]:
        match_learnwares = []
        for learnware in learnware_list:
            if learnware_id == learnware.id:
                match_learnwares.append(learnware)
        return match_learnwares

    def _match_semantic_spec(self, semantic_spec1, semantic_spec2):
        """
        semantic_spec1: semantic spec input by user
        semantic_spec2: semantic spec in database
        """
        if semantic_spec1.keys() != semantic_spec2.keys():
            # sematic spec in database may contain more keys than user input
            pass

        name2 = semantic_spec2["Name"]["Values"].lower()
        description2 = semantic_spec2["Description"]["Values"].lower()

        for key in semantic_spec1.keys():
            v1 = semantic_spec1[key].get("Values", "")
            if key not in semantic_spec2 or len(v1) == 0:
                continue

            v2 = semantic_spec2[key].get("Values", "")
            if key in ("Name", "Description"):
                v1 = v1.lower()
                if v1 not in name2 and v1 not in description2:
                    return False
            else:
                if len(v2) == 0:
                    # user input contains some key that is not in database
                    return False

                if semantic_spec1[key]["Type"] == "Class":
                    if isinstance(v2, list):
                        v2 = v2[0]
                    if v2 not in v1:
                        return False
                elif semantic_spec1[key]["Type"] == "Tag":
                    if not (set(v1) & set(v2)):
                        return False

        return True

    def __call__(self, learnware_list: List[Learnware], user_info: BaseUserInfo) -> SearchResults:
        match_learnwares = []
        user_semantic_spec = user_info.get_semantic_spec()

        # Learnware id search
        if "learnware_id" in user_semantic_spec:
            learnware_list = self._learnware_id_search(user_semantic_spec["learnware_id"]["Values"], learnware_list)

        # Semantic tag match
        for learnware in learnware_list:
            learnware_semantic_spec = learnware.get_specification().get_semantic_spec()
            if self._match_semantic_spec(user_semantic_spec, learnware_semantic_spec):
                match_learnwares.append(learnware)
        logger.info("semantic_spec search: choose %d from %d learnwares" % (len(match_learnwares), len(learnware_list)))
        return SearchResults(single_results=[SingleSearchItem(learnware=_learnware) for _learnware in match_learnwares])


class EasyFuzzSemanticSearcher(AtomicSearcher):
    def is_applicable_learnware(self, learnware: Learnware) -> bool:
        return True

    def is_applicable_user(self, user_info: BaseUserInfo) -> bool:
        return True

    def _learnware_id_search(self, learnware_id: str, learnware_list: List[Learnware]) -> List[Learnware]:
        match_learnwares = []
        for learnware in learnware_list:
            if learnware_id in learnware.id:
                match_learnwares.append(learnware)
        return match_learnwares

    def _match_semantic_spec_tag(self, semantic_spec1, semantic_spec2) -> bool:
        """Judge if tags of two semantic specs are consistent

        Parameters
        ----------
        semantic_spec1 :
            semantic spec input by user
        semantic_spec2 :
            semantic spec in database

        Returns
        -------
        bool
            consistent (True) or not consistent (False)
        """
        for key in semantic_spec1.keys():
            v1 = semantic_spec1[key].get("Values", "")
            if len(v1) == 0:
                continue
            
            if key not in semantic_spec2:
                if "Others" in v1:
                    # v1 contains "Others" and key not in semantic_spec2
                    continue
                else:
                    # user input contains some key that is not in database
                    return False
            
            v2 = semantic_spec2[key].get("Values", "")
            if key not in ("Name", "Description"):
                if len(v2) == 0:
                    # user input contains some key that is not in database
                    return False

                if semantic_spec1[key]["Type"] in ("Class", "Optional"):
                    if isinstance(v2, list):
                        v2 = v2[0]
                    if v2 not in v1:
                        return False
                elif semantic_spec1[key]["Type"] == "Tag":
                    if not (set(v1) & set(v2)):
                        return False
        return True

    def __call__(
        self, learnware_list: List[Learnware], user_info: BaseUserInfo, max_num: int = 50000, min_score: float = 75.0
    ) -> SearchResults:
        """Search learnware by fuzzy matching of semantic spec

        Parameters
        ----------
        learnware_list : List[Learnware]
            The list of learnwares
        user_info : BaseUserInfo
            user_info contains semantic_spec
        max_num : int, optional
            maximum number of learnwares returned, by default 50000
        min_score : float, optional
            Minimum fuzzy matching score of learnwares returned, by default 30.0

        Returns
        -------
        List[Learnware]
            The list of returned learnwares
        """
        matched_learnware_tag = []
        final_result = []
        user_semantic_spec = user_info.get_semantic_spec()

        # Learnware id search
        if "learnware_id" in user_semantic_spec:
            learnware_list = self._learnware_id_search(user_semantic_spec["learnware_id"]["Values"], learnware_list)

        # Semantic tag match
        for learnware in learnware_list:
            learnware_semantic_spec = learnware.get_specification().get_semantic_spec()
            if self._match_semantic_spec_tag(user_semantic_spec, learnware_semantic_spec):
                matched_learnware_tag.append(learnware)

        if len(matched_learnware_tag) > 0:
            if "Name" in user_semantic_spec:
                name_user = user_semantic_spec["Name"]["Values"].lower()
                if len(name_user) > 0:
                    # Exact search
                    name_list = [
                        learnware.get_specification().get_semantic_spec()["Name"]["Values"].lower()
                        for learnware in matched_learnware_tag
                    ]
                    des_list = [
                        learnware.get_specification().get_semantic_spec()["Description"]["Values"].lower()
                        for learnware in matched_learnware_tag
                    ]

                    matched_learnware_exact = []
                    for i in range(len(name_list)):
                        if name_user in name_list[i] or name_user in des_list[i]:
                            matched_learnware_exact.append(matched_learnware_tag[i])

                    if len(matched_learnware_exact) == 0:
                        # Fuzzy search
                        matched_learnware_fuzz, fuzz_scores = [], []
                        for i in range(len(name_list)):
                            score_name = fuzz.partial_ratio(name_user, name_list[i])
                            score_des = fuzz.partial_ratio(name_user, des_list[i])
                            final_score = max(score_name, score_des)
                            if final_score >= min_score:
                                matched_learnware_fuzz.append(matched_learnware_tag[i])
                                fuzz_scores.append(final_score)

                        # Sort by score
                        sort_idx = sorted(list(range(len(fuzz_scores))), key=lambda k: fuzz_scores[k], reverse=True)[
                            :max_num
                        ]
                        final_result = [matched_learnware_fuzz[idx] for idx in sort_idx]
                    else:
                        final_result = matched_learnware_exact
                else:
                    final_result = matched_learnware_tag
            else:
                final_result = matched_learnware_tag

        logger.info("semantic_spec search: choose %d from %d learnwares" % (len(final_result), len(learnware_list)))
        return SearchResults(single_results=[SingleSearchItem(learnware=_learnware) for _learnware in final_result])


class EasyStatSearcher(AtomicSearcher):
    SPEC_TYPES = ["RKMETableSpecification", "RKMEImageSpecification", "RKMETextSpecification"]

    def is_applicable_learnware(self, learnware: Learnware) -> bool:
        return any(spec_type in learnware.specification.stat_spec for spec_type in self.SPEC_TYPES)

    def is_applicable_user(self, user_info: BaseUserInfo) -> bool:
        for spec_type in self.SPEC_TYPES:
            if spec_type in user_info.stat_info:
                user_rkme = user_info.stat_info[spec_type]

                if np.isfinite(float(user_rkme.dist(user_rkme))):
                    return True

        return False

    def _convert_dist_to_score(
        self, dist_list: List[float], dist_ratio: float = 0.1, min_score: float = 0.92, improve_score: float = 0.7
    ) -> List[float]:
        """Convert mmd dist list into min_max score list

        Parameters
        ----------
        dist_list : List[float]
            The list of mmd distances from learnware rkmes to user rkme
        dist_ratio: float
            The paramter for converting mmd dist to score
        min_score: float
            The minimum score for maximum returned score
        improve_score: float
            The learnware score lower than improve_score will be improved

        Returns
        -------
        List[float]
            The list of min_max scores of each learnware
        """
        if len(dist_list) == 0:
            return []

        min_dist, max_dist = min(dist_list), max(dist_list)
        if min_dist == max_dist:
            return [1 for dist in dist_list]
        else:
            avg_dist = sum(dist_list) / len(dist_list)
            dist_epsilon = avg_dist * dist_ratio
            max_score = (max_dist - min_dist) / (max_dist - dist_epsilon)

            if min_dist < dist_epsilon:
                dist_epsilon = min_dist
            elif max_score < min_score:
                dist_epsilon = max_dist - (max_dist - min_dist) / min_score

            score_list = []
            for dist in dist_list:
                score = (max_dist - dist) / (max_dist - dist_epsilon)
                if score < improve_score:
                    score = min(math.sqrt(score), improve_score)
                score_list.append(score)

            return score_list

    def _calculate_rkme_spec_mixture_weight(
        self,
        learnware_list: List[Learnware],
        user_rkme: RKMETableSpecification,
        intermediate_K: np.ndarray = None,
        intermediate_C: np.ndarray = None,
    ) -> Tuple[List[float], float]:
        """Calculate mixture weight for the learnware_list based on a user's rkme

        Parameters
        ----------
        learnware_list : List[Learnware]
            A list of existing learnwares
        user_rkme : RKMETableSpecification
            User RKME statistical specification
        intermediate_K : np.ndarray, optional
            Intermediate kernel matrix K, by default None
        intermediate_C : np.ndarray, optional
            Intermediate inner product vector C, by default None

        Returns
        -------
        Tuple[List[float], float]
            The first is the list of mixture weights
            The second is the mmd dist between the mixture of learnware rkmes and the user's rkme
        """
        learnware_num = len(learnware_list)
        RKME_list = [learnware.specification.get_stat_spec_by_name(self.stat_spec_type) for learnware in learnware_list]

        if isinstance(intermediate_K, np.ndarray):
            K = intermediate_K
        else:
            K = np.zeros((learnware_num, learnware_num))
            for i in range(K.shape[0]):
                K[i, i] = RKME_list[i].inner_prod(RKME_list[i])
                for j in range(i + 1, K.shape[0]):
                    K[i, j] = K[j, i] = RKME_list[i].inner_prod(RKME_list[j])

        if isinstance(intermediate_C, np.ndarray):
            C = intermediate_C
        else:
            C = np.zeros((learnware_num, 1))
            for i in range(C.shape[0]):
                C[i, 0] = user_rkme.inner_prod(RKME_list[i])

        K = torch.from_numpy(K).double().to(user_rkme.device)
        C = torch.from_numpy(C).double().to(user_rkme.device)

        # beta can be negative
        # weight = torch.linalg.inv(K + torch.eye(K.shape[0]).to(user_rkme.device) * 1e-5) @ C

        # beta must be nonnegative
        weight, obj = rkme_solve_qp(K, C)
        weight = weight.double().to(user_rkme.device)
        score = user_rkme.inner_prod(user_rkme) + 2 * obj
        return weight.detach().cpu().numpy().reshape(-1), score

    def _calculate_intermediate_K_and_C(
        self,
        learnware_list: List[Learnware],
        user_rkme: RKMETableSpecification,
        intermediate_K: np.ndarray = None,
        intermediate_C: np.ndarray = None,
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Incrementally update the values of intermediate_K and intermediate_C

        Parameters
        ----------
        learnware_list : List[Learnware]
            The list of learnwares up till now
        user_rkme : RKMETableSpecification
            User RKME statistical specification
        intermediate_K : np.ndarray, optional
            Intermediate kernel matrix K, by default None
        intermediate_C : np.ndarray, optional
            Intermediate inner product vector C, by default None

        Returns
        -------
        Tuple[np.ndarray, np.ndarray]
            The first is the intermediate value of K
            The second is the intermediate value of C
        """
        num = intermediate_K.shape[0] - 1
        RKME_list = [learnware.specification.get_stat_spec_by_name(self.stat_spec_type) for learnware in learnware_list]
        for i in range(intermediate_K.shape[0]):
            intermediate_K[num, i] = intermediate_K[i, num] = RKME_list[-1].inner_prod(RKME_list[i])
        intermediate_C[num, 0] = user_rkme.inner_prod(RKME_list[-1])
        return intermediate_K, intermediate_C

    def _search_by_rkme_spec_mixture_auto(
        self,
        learnware_list: List[Learnware],
        user_rkme: RKMETableSpecification,
        max_search_num: int,
        weight_cutoff: float = 0.98,
    ) -> Tuple[Optional[float], List[float], List[Learnware]]:
        """Select learnwares based on a total mixture ratio, then recalculate their mixture weights

        Parameters
        ----------
        learnware_list : List[Learnware]
            The list of learnwares whose mixture approximates the user's rkme
        user_rkme : RKMETableSpecification
            User RKME statistical specification
        max_search_num : int
            The maximum number of the returned learnwares
        weight_cutoff : float, optional
            The ratio for selecting out the mose relevant learnwares, by default 0.9

        Returns
        -------
        Tuple[float, List[float], List[Learnware]]
            The first is the mixture mmd dist
            The second is the list of weight
            The third is the list of Learnware
        """
        learnware_num = len(learnware_list)
        if learnware_num == 0:
            return None, [], []
        if learnware_num < max_search_num:
            logger.warning("Available Learnware num less than search_num!")
            max_search_num = learnware_num

        weight, _ = self._calculate_rkme_spec_mixture_weight(learnware_list, user_rkme)
        sort_by_weight_idx_list = sorted(range(learnware_num), key=lambda k: weight[k], reverse=True)

        weight_sum = 0
        mixture_list = []
        for idx in sort_by_weight_idx_list:
            weight_sum += weight[idx]
            if weight_sum <= weight_cutoff:
                mixture_list.append(learnware_list[idx])
            else:
                break

        if len(mixture_list) <= 1:
            mixture_list = [learnware_list[sort_by_weight_idx_list[0]]]
            mixture_weight = [1.0]
            mmd_dist = user_rkme.dist(mixture_list[0].specification.get_stat_spec_by_name(self.stat_spec_type))
        else:
            if len(mixture_list) > max_search_num:
                mixture_list = mixture_list[:max_search_num]
            mixture_weight, mmd_dist = self._calculate_rkme_spec_mixture_weight(mixture_list, user_rkme)

        return mmd_dist, mixture_weight, mixture_list

    def _filter_by_rkme_spec_single(
        self,
        sorted_score_list: List[float],
        learnware_list: List[Learnware],
        filter_score: float = 0.6,
        min_num: int = 1,
    ) -> Tuple[List[float], List[Learnware]]:
        """Filter search result of _search_by_rkme_spec_single

        Parameters
        ----------
        sorted_score_list : List[float]
            The list of score transformed by mmd dist
        learnware_list : List[Learnware]
            The list of learnwares whose mixture approximates the user's rkme
        filter_score: float
            The learnware whose score is lower than filter_score will be filtered
        min_num: int
            The minimum number of returned learnwares

        Returns
        -------
        Tuple[List[float], List[Learnware]]
            the first is the list of score
            the second is the list of Learnware
        """
        idx = min(min_num, len(learnware_list))
        while idx < len(learnware_list):
            if sorted_score_list[idx] < filter_score:
                break
            idx = idx + 1
        return sorted_score_list[:idx], learnware_list[:idx]

    def _filter_by_rkme_spec_metadata(
        self,
        learnware_list: List[Learnware],
        user_rkme: Union[RKMETableSpecification, RKMEImageSpecification, RKMETextSpecification],
    ) -> List[Learnware]:
        """Filter learnwares whose rkme metadata different from user_rkme

        Parameters
        ----------
        learnware_list : List[Learnware]
            The list of learnwares whose mixture approximates the user's rkme
        user_rkme : Union[RKMETableSpecification, RKMEImageSpecification, RKMETextSpecification]
            User RKME statistical specification

        Returns
        -------
        List[Learnware]
            Learnwares whose rkme dimensions equal user_rkme in user_info
        """
        filtered_learnware_list = []
        user_rkme_dim = str(list(user_rkme.get_z().shape)[1:])

        for learnware in learnware_list:
            if self.stat_spec_type not in learnware.specification.stat_spec:
                continue
            rkme = learnware.specification.get_stat_spec_by_name(self.stat_spec_type)
            if self.stat_spec_type == "RKMETextSpecification" and not set(user_rkme.language).issubset(
                set(rkme.language)
            ):
                continue

            rkme_dim = str(list(rkme.get_z().shape)[1:])
            if rkme_dim == user_rkme_dim:
                filtered_learnware_list.append(learnware)

        return filtered_learnware_list

    def _search_by_rkme_spec_mixture_greedy(
        self,
        learnware_list: List[Learnware],
        user_rkme: RKMETableSpecification,
        max_search_num: int,
        decay_rate: float = 0.95,
    ) -> Tuple[Optional[float], List[float], List[Learnware]]:
        """Greedily match learnwares such that their mixture become closer and closer to user's rkme

        Parameters
        ----------
        learnware_list : List[Learnware]
            The list of learnwares whose mixture approximates the user's rkme
        user_rkme : RKMETableSpecification
            User RKME statistical specification
        max_search_num : int
            The maximum number of the returned learnwares
        decay_rate: float
            The decrease ratio of minimum mmd dist to stop further rkme_spec matching

        Returns
        -------
        Tuple[float, List[float], List[Learnware]]
            The first is the mixture mmd dist
            The second is the list of weight
            The third is the list of Learnware
        """
        learnware_num = len(learnware_list)
        if learnware_num == 0:
            return None, [], []
        if learnware_num < max_search_num:
            logger.warning("Available Learnware num less than search_num!")
            max_search_num = learnware_num

        flag_list = [0 for _ in range(learnware_num)]
        mixture_list, weight_list, mmd_dist = [], [], None
        intermediate_K, intermediate_C = np.zeros((1, 1)), np.zeros((1, 1))

        for k in range(max_search_num):
            idx_min, score_min = None, None
            weight_min = None
            mixture_list.append(None)

            if k != 0:
                intermediate_K = np.c_[intermediate_K, np.zeros((k, 1))]
                intermediate_K = np.r_[intermediate_K, np.zeros((1, k + 1))]
                intermediate_C = np.r_[intermediate_C, np.zeros((1, 1))]

            for idx in range(len(learnware_list)):
                if flag_list[idx] == 0:
                    mixture_list[-1] = learnware_list[idx]
                    intermediate_K, intermediate_C = self._calculate_intermediate_K_and_C(
                        mixture_list, user_rkme, intermediate_K, intermediate_C
                    )
                    weight, score = self._calculate_rkme_spec_mixture_weight(
                        mixture_list, user_rkme, intermediate_K, intermediate_C
                    )
                    if score_min is None or score < score_min:
                        idx_min, score_min, weight_min = idx, score, weight

            if mmd_dist is None or score_min <= mmd_dist * decay_rate:
                mmd_dist, weight_list = score_min, weight_min
                mixture_list[-1] = learnware_list[idx_min]
                flag_list[idx_min] = 1
                intermediate_K, intermediate_C = self._calculate_intermediate_K_and_C(
                    mixture_list, user_rkme, intermediate_K, intermediate_C
                )
            else:
                mixture_list = mixture_list[:-1]
                break

        return mmd_dist, weight_list, mixture_list

    def _search_by_rkme_spec_single(
        self,
        learnware_list: List[Learnware],
        user_rkme: Union[RKMETableSpecification, RKMEImageSpecification, RKMETextSpecification],
    ) -> Tuple[List[float], List[Learnware]]:
        """Calculate the distances between learnwares in the given learnware_list and user_rkme

        Parameters
        ----------
        learnware_list : List[Learnware]
            The list of learnwares whose mixture approximates the user's rkme
        user_rkme : Union[RKMETableSpecification, RKMEImageSpecification, RKMETextSpecification]
            user RKME statistical specification

        Returns
        -------
        Tuple[List[float], List[Learnware]]
            the first is the list of mmd dist
            the second is the list of Learnware
            both lists are sorted by mmd dist
        """
        rkme_list = [learnware.specification.get_stat_spec_by_name(self.stat_spec_type) for learnware in learnware_list]
        filtered_idx_list, mmd_dist_list = [], []
        for idx in range(len(rkme_list)):
            mmd_dist = float(rkme_list[idx].dist(user_rkme))
            if np.isfinite(mmd_dist):
                mmd_dist_list.append(mmd_dist)
                filtered_idx_list.append(idx)
            else:
                logger.warning(
                    f"The distance between user_spec and learnware_spec (id: {learnware_list[idx].id}) is not finite, where distance is {mmd_dist}"
                )

        sorted_idx_list = sorted(range(len(mmd_dist_list)), key=lambda k: mmd_dist_list[k])
        sorted_dist_list = [mmd_dist_list[idx] for idx in sorted_idx_list]
        sorted_learnware_list = [learnware_list[filtered_idx_list[idx]] for idx in sorted_idx_list]

        return sorted_dist_list, sorted_learnware_list

    def __call__(
        self,
        learnware_list: List[Learnware],
        user_info: BaseUserInfo,
        max_search_num: int = 5,
        search_method: str = "greedy",
    ) -> SearchResults:
        self.stat_spec_type = parse_specification_type(stat_specs=user_info.stat_info, spec_list=self.SPEC_TYPES)

        user_rkme = user_info.stat_info[self.stat_spec_type]

        learnware_list = self._filter_by_rkme_spec_metadata(learnware_list, user_rkme)
        logger.info(f"After filter by rkme dimension, learnware_list length is {len(learnware_list)}")

        sorted_dist_list, single_learnware_list = self._search_by_rkme_spec_single(learnware_list, user_rkme)
        if len(single_learnware_list) == 0:
            return SearchResults()

        processed_learnware_list = single_learnware_list[: max_search_num * max_search_num]
        if sorted_dist_list[0] > 0 and search_method == "auto":
            mixture_dist, weight_list, mixture_learnware_list = self._search_by_rkme_spec_mixture_auto(
                processed_learnware_list, user_rkme, max_search_num
            )
        elif sorted_dist_list[0] > 0 and search_method == "greedy":
            mixture_dist, weight_list, mixture_learnware_list = self._search_by_rkme_spec_mixture_greedy(
                processed_learnware_list, user_rkme, max_search_num
            )
        else:
            if search_method not in ["auto", "greedy"]:
                logger.warning(f"{search_method} not supported!")
            mixture_dist, weight_list, mixture_learnware_list = None, [], []

        # Check the length of mixture learnware list
        if len(mixture_learnware_list) == 1:
            mixture_dist, weight_list, mixture_learnware_list = None, [], []

        # Special Transform for ImageSpecification
        if self.stat_spec_type == "RKMEImageSpecification":
            sorted_dist_list = [1 - np.exp(-d / 0.00005) for d in sorted_dist_list]
            if mixture_dist is not None:
                mixture_dist = 1 - np.exp(-mixture_dist / 0.00005)

        if mixture_dist is None:
            sorted_score_list = self._convert_dist_to_score(sorted_dist_list)
            mixture_score = None
        else:
            merge_score_list = self._convert_dist_to_score(sorted_dist_list + [mixture_dist])
            sorted_score_list = merge_score_list[:-1]
            mixture_score = merge_score_list[-1]
            if int(mixture_score * 100) == int(sorted_score_list[0] * 100):
                mixture_score = None
                mixture_learnware_list = []
        logger.info(
            f"After search by rkme spec, learnware_list length is {len(learnware_list)}, mixture_learnware_list length is {len(mixture_learnware_list)}"
        )

        # Filter learnware with low score
        sorted_score_list, single_learnware_list = self._filter_by_rkme_spec_single(
            sorted_score_list, single_learnware_list
        )
        if len(single_learnware_list) == 1 and sorted_score_list[0] < 0.6:
            ratio = 100 if abs(sorted_score_list[0]) < 1e-5 else 0.6 / sorted_score_list[0]
            sorted_score_list[0] = 0.6
            mixture_score = min(1, mixture_score * ratio) if mixture_score is not None else None
        logger.info(f"After filter by rkme spec, learnware_list length is {len(learnware_list)}")

        search_results = SearchResults()

        search_results.update_single_results(
            [
                SingleSearchItem(learnware=_learnware, score=_score)
                for _score, _learnware in zip(sorted_score_list, single_learnware_list)
            ]
        )
        if mixture_score is not None and len(mixture_learnware_list) > 0:
            search_results.update_multiple_results(
                [MultipleSearchItem(learnwares=mixture_learnware_list, score=mixture_score)]
            )
        return search_results


class SeqCombinedSearcher(BaseSearcher):
    def __init__(
        self,
        organizer: BaseOrganizer,
        semantic_searcher_list: List[AtomicSearcher],
        stat_searcher_list: List[AtomicSearcher],
    ):
        self.semantic_searcher_list = semantic_searcher_list
        self.stat_searcher_list = stat_searcher_list
        super(SeqCombinedSearcher, self).__init__(organizer)

    def reset(self, organizer: BaseOrganizer):
        self.learnware_organizer = organizer
        for searcher in self.semantic_searcher_list + self.stat_searcher_list:
            searcher.reset(organizer)

    def __call__(
        self, user_info: BaseUserInfo, check_status: int = None, max_search_num: int = 5, search_method: str = "greedy"
    ) -> SearchResults:
        """
        Search learnwares based on user_info, iterating over semantic and stat searchers to find applicable results.

        Parameters
        ----------
        user_info : BaseUserInfo
            The user information for searching learnwares.
        max_search_num : int, optional
            The maximum number of the returned learnwares.
        check_status : int, optional
            - None: search from all learnwares
            - Others: search from learnwares with check_status.

        Returns
        -------
        SearchResults
            The search results, including sorted lists of learnwares and associated scores.
        """
        learnware_list = self.learnware_organizer.get_learnwares(check_status=check_status)

        for semantic_searcher in self.semantic_searcher_list:
            if semantic_searcher.is_applicable_user(user_info):
                filtered_learnware_list = [
                    learnware for learnware in learnware_list if semantic_searcher.is_applicable_learnware(learnware)
                ]
                semantic_search_result = semantic_searcher(filtered_learnware_list, user_info)
                learnware_list = [search_item.learnware for search_item in semantic_search_result.get_single_results()]
                break

        if len(learnware_list) == 0:
            return SearchResults()

        for stat_searcher in self.stat_searcher_list:
            if stat_searcher.is_applicable_user(user_info):
                filtered_learnware_list = [
                    learnware for learnware in learnware_list if stat_searcher.is_applicable_learnware(learnware)
                ]
                return stat_searcher(filtered_learnware_list, user_info, max_search_num, search_method)

        return semantic_search_result
