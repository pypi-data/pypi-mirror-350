import copy
from dataclasses import dataclass
from dataclasses import field as dataclass_field
from typing import List

import awkward as ak
import numba
import numpy as np

from f9columnar.processors_collection import Cut
from f9columnar.utils.ak_helpers import ak_unique

TRIGGER_PT = {
    "ptBaseline": 30.0,
    "ptBaselineLow": 10.0,
    "pt10": 11.0,
    "pt12": 13.0,
    "pt14": 15.0,
    "pt15": 16.0,
    "pt17": 18.0,
    "pt18": 19.0,
    "pt20": 21.0,
    "pt22": 23.0,
    "pt24": 25.0,
    "pt26": 27.0,
    "pt28": 29.0,
    "pt60": 65.0,
    "pt70": 75.0,
    "pt80": 85.0,
    "pt100": 105.0,
    "pt120": 126.0,
    "pt140": 147.0,
    "pt160": 168.0,
    "ptUnprescaledEl": 315.0,
    "ptMax": np.inf,
}


@numba.njit
def _matched_mask_reshape(event_nums, matched_mask, array_builder):
    for e, event_mask in enumerate(matched_mask):
        zero_event = np.zeros(event_nums[e], dtype=numba.boolean)

        for i in event_mask:
            zero_event[int(i)] = True

        array_builder.begin_list()
        for j in zero_event:
            array_builder.append(j)
        array_builder.end_list()

    return array_builder


def matched_mask_reshape(pt_array, matched_mask):
    """Reshapes matched mask to match particle numbers in event by masking out unmatched particles.

    Parameters
    ----------
    pt_array : ak.Array
        Representative array to get event numbers.
    matched_mask : ak.Array
        Masked array of matched particles.

    Returns
    -------
    ak.Array
        Boolean array of matched particles.
    """
    event_nums = ak.num(pt_array)

    builder = ak.ArrayBuilder()
    _matched_mask_reshape(event_nums, matched_mask, builder)

    array = builder.snapshot()
    return array


@dataclass
class Trigger:
    trigger_name: str
    year: int
    obj_name: str = ""
    pt_low: float | str = 0.0
    pt_high: float | str = np.inf
    prescale: bool = False

    is_joined = False

    def get_single_branches(self, as_dict=False):
        branches = (
            f"trigPassed_{self.trigger_name}",
            f"{self.obj_name}_matched_{self.trigger_name}",
        )

        if as_dict:
            return {self.trigger_name: branches}
        else:
            return branches

    def get_di_branches(self, as_dict=False):
        branches = (
            f"trigPassed_{self.trigger_name}",
            f"trigMatchedPairs_{self.trigger_name}.first",
            f"trigMatchedPairs_{self.trigger_name}.second",
        )

        if as_dict:
            return {self.trigger_name: branches}
        else:
            return branches

    def get_prescale_branches(self, as_dict=False):
        if self.prescale:
            branch = f"trigPrescale_{self.trigger_name}"
        else:
            branch = None

        if as_dict:
            return {self.trigger_name: branch}
        else:
            return branch

    def _get_pt_thresholds(self):
        if type(self.pt_low) is float:
            low = self.pt_low
        else:
            low = TRIGGER_PT[self.pt_low]

        if type(self.pt_high) is float:
            high = self.pt_high
        else:
            high = TRIGGER_PT[self.pt_high]

        return low * 1e3, high * 1e3

    def __post_init__(self):
        self.pt_low, self.pt_high = self._get_pt_thresholds()


@dataclass
class JoinedTrigger:
    triggers: List[Trigger]
    trigger_name: List[str] = dataclass_field(default_factory=list)
    year: int | None = None
    obj_name: str = ""
    pt_low: float = 0.0
    pt_high: float = np.inf
    prescale: bool = False

    is_joined = True

    def get_single_branches(self, as_dict=False):
        if as_dict:
            branches = {}
            for trigger in self.triggers:
                branches[trigger.trigger_name] = trigger.get_single_branches(as_dict=False)
        else:
            branches = []
            for trigger in self.triggers:
                branches.extend(trigger.get_single_branches())

        return branches

    def get_di_branches(self, as_dict=False):
        if as_dict:
            branches = {}
            for trigger in self.triggers:
                branches[trigger.trigger_name] = trigger.get_di_branches(as_dict=False)
        else:
            branches = []
            for trigger in self.triggers:
                branches.extend(trigger.get_di_branches())

        return branches

    def get_prescale_branches(self, as_dict=False):
        if as_dict:
            branches = {}
            for trigger in self.triggers:
                branches[trigger.trigger_name] = trigger.get_prescale_branch()
        else:
            branches = []
            for trigger in self.triggers:
                branches.append(trigger.get_prescale_branch())

        return branches

    def _get_pt_thresholds(self):
        lows, highs = [], []
        for trigger in self.triggers:
            low, high = trigger._get_pt_thresholds()
            lows.append(low)
            highs.append(high)

        return min(lows), max(highs)

    def __post_init__(self):
        self.pt_low, self.pt_high = self._get_pt_thresholds()

        trigger_name = []
        for trigger in self.triggers:
            trigger_name.append(trigger.trigger_name)
        self.trigger_name = "|".join(trigger_name)

        years = set()
        for trigger in self.triggers:
            years.add(trigger.year)

        assert len(years) == 1, "All triggers in a joined trigger must have the same year."
        self.year = years.pop()

        obj_names = set()
        for trigger in self.triggers:
            obj_names.add(trigger.obj_name)

        assert len(obj_names) == 1, "All triggers in a joined trigger must have the same object name."
        self.obj_name = obj_names.pop()


@dataclass
class TriggerChain:
    chain: list

    def __post_init__(self):
        chain = []
        for trigger in self.chain:
            if type(trigger) is list:
                chain.append(JoinedTrigger(trigger))
            else:
                chain.append(trigger)

        self.chain = chain


class BaseTriggerCut(Cut):
    name = "baseTriggerCut"
    trigger_type = None
    triggers = None

    def __init__(self, obj_name, pt_branch=None):
        super().__init__()
        self.trigger_chain = TriggerChain(self.triggers)

        self.obj_name = obj_name

        if pt_branch is None:
            self.pt_branch = f"{obj_name}_pt_NOSYS"
        else:
            self.pt_branch = pt_branch

        for trigger in self.trigger_chain.chain:
            trigger.obj_name = obj_name

        self.branch_name, self.prescale_branches = self._handle_branch_names()

        if len(self.prescale_branches) == 0:
            self.disable_prescales = True
        else:
            self.disable_prescales = False

    def _handle_branch_names(self):
        branch_name, prescale_branches = [], []

        for trigger in self.trigger_chain.chain:
            if self.trigger_type == "single":
                branch_name.extend(trigger.get_single_branches())
            elif self.trigger_type == "di":
                branch_name.extend(trigger.get_di_branches())
            else:
                raise ValueError(f"Invalid trigger type {self.trigger_type}.")

            if trigger.prescale:
                prescale_branch = trigger.get_prescale_branches()
                branch_name.append(prescale_branch)
                prescale_branches.append(prescale_branch)

        branch_name = sorted(list(set(branch_name)))

        return branch_name, prescale_branches

    def _trigger_single_masks(self, trigger, arrays):
        branches = trigger.get_single_branches(as_dict=True)

        combined_passed_mask, combined_matched_mask = None, None
        for i, branch_tuple in enumerate(branches.values()):
            passed_branch, matched_branch = branch_tuple

            passed_mask = arrays[passed_branch]

            matched_mask = ak.values_astype(arrays[matched_branch], bool)

            if i == 0:
                combined_passed_mask, combined_matched_mask = passed_mask, matched_mask
            else:
                combined_passed_mask = combined_passed_mask | passed_mask
                combined_matched_mask = combined_matched_mask | matched_mask

        return combined_passed_mask, combined_matched_mask

    def _trigger_di_masks(self, trigger, arrays):
        branches = trigger.get_di_branches(as_dict=True)

        combined_passed_mask, combined_matched_mask = None, []
        for i, branch_tuple in enumerate(branches.values()):
            passed_branch, matched_branch_first, matched_branch_second = branch_tuple

            passed_mask = arrays[passed_branch]

            matched_first = arrays[matched_branch_first]
            matched_second = arrays[matched_branch_second]

            matched_both = ak.concatenate([matched_first, matched_second], axis=1)
            matched_both = ak_unique(matched_both)

            combined_matched_mask.append(matched_both)

            if i == 0:
                combined_passed_mask = passed_mask
            else:
                combined_passed_mask = combined_passed_mask | passed_mask

        if len(combined_matched_mask) > 1:
            combined_matched_mask = ak.concatenate(combined_matched_mask, axis=1)
            combined_matched_mask = ak_unique(combined_matched_mask)
        else:
            combined_matched_mask = combined_matched_mask[0]

        combined_matched_mask = matched_mask_reshape(arrays[self.pt_branch], combined_matched_mask)

        return combined_passed_mask, combined_matched_mask

    def _run_triggers(self, arrays, years):
        # this processor requires ArrayProcessor to run first
        has_groups = hasattr(arrays, "group_arrays")

        pt = arrays[self.pt_branch]

        if has_groups:
            arrays[self.obj_name, f"{self.obj_name}_idx"] = np.arange(len(pt))
        else:
            arrays[f"{self.obj_name}_idx"] = np.arange(len(pt))

        idx_lst, prescales_lst = [], []

        for trigger in self.trigger_chain.chain:
            # year
            year_mask = years == trigger.year

            if not ak.any(year_mask):
                continue

            year_mask = ak.values_astype(year_mask, bool)

            # pt
            pt_low, pt_high = trigger.pt_low, trigger.pt_high
            pt_mask = (pt >= pt_low) & (pt <= pt_high)

            # passed and matched
            if self.trigger_type == "single":
                passed_mask, matched_mask = self._trigger_single_masks(trigger, arrays)
            elif self.trigger_type == "di":
                passed_mask, matched_mask = self._trigger_di_masks(trigger, arrays)
            else:
                pass

            passed_mask = ak.values_astype(passed_mask, bool)

            total_mask = year_mask & pt_mask & passed_mask & matched_mask

            # get the passed indices from the total mask and save them
            idx_arrays = copy.deepcopy(arrays)

            if has_groups:
                idx_arrays[self.obj_name] = idx_arrays[self.obj_name][total_mask]
                idx_arrays["other"] = idx_arrays["other"][total_mask]
                idx_arrays = idx_arrays.remove_empty(self.obj_name)
            else:
                idx_arrays = idx_arrays[total_mask]
                idx_arrays = idx_arrays.remove_empty()

            idx = idx_arrays[f"{self.obj_name}_idx"]
            idx_lst.append(idx)

            # handle prescales if needed
            if self.is_data and not self.disable_prescales:
                prescale_branch = trigger.get_prescale_branches()
                prescales = idx_arrays[prescale_branch]

                prescales_lst.append(prescales)

        # the actual masking happens here
        passed_idx = np.concatenate(idx_lst)

        _, unique_idx = np.unique(passed_idx, return_index=True)
        passed_idx = passed_idx[unique_idx]

        arrays = arrays[passed_idx]

        if self.is_data and not self.disable_prescales:
            prescales = np.concatenate(prescales_lst)
            prescales = prescales[unique_idx]

            if has_groups:
                arrays[self.obj_name, f"{self.obj_name}_prescale"] = prescales
            else:
                arrays[f"{self.obj_name}_prescale"] = prescales

        return arrays

    def _run_single_triggers(self, arrays):
        years = ak.to_numpy(arrays["years"])

        # remove accidental prescales on single triggers
        if self.trigger_type == "single":
            accidental_prescale = [170, 171, 172]
            for p in accidental_prescale:
                years = np.where(years == p, 17, years)

        return self._run_triggers(arrays, years)

    def _run_di_triggers(self, arrays):
        years = ak.to_numpy(arrays["years"])
        return self._run_triggers(arrays, years)

    def run(self, arrays):
        if len(arrays) == 0:
            if not self.disable_prescales:
                arrays[f"prescale_{self.obj_name}"] = ak.values_astype(ak.ones_like(arrays["years"]), float)

            return {"arrays": arrays}

        if self.trigger_type == "single":
            arrays = self._run_single_triggers(arrays)
        elif self.trigger_type == "di":
            arrays = self._run_di_triggers(arrays)
        else:
            pass

        return {"arrays": arrays}
