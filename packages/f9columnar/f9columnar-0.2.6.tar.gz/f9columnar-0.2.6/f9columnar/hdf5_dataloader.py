from __future__ import annotations

import copy
import json
import logging
import os
from collections.abc import Callable
from itertools import product
from typing import Any

import h5py
import numpy as np
import pandas as pd
import torch
from numpy.typing import ArrayLike
from torch import multiprocessing
from torch.utils.data import DataLoader, IterableDataset

from f9columnar.processors import Processor, ProcessorsGraph
from f9columnar.utils.helpers import get_file_size


class Hdf5Iterator:
    def __init__(
        self,
        file: str,
        chunk_size: int | None,
        start_entry: int,
        stop_entry: int,
        shuffle: bool = False,
        holdout_range: tuple[float, float] | None = None,
    ) -> None:
        self.file = file
        self.start_entry = start_entry
        self.stop_entry = stop_entry
        self.shuffle = shuffle

        if chunk_size is None:
            self.chunk_size = self.stop_entry - self.start_entry
        else:
            self.chunk_size = chunk_size

        self.file, self.dataset_name = self.file.split(":")

        self.handle = h5py.File(self.file, "r")

        if holdout_range is not None:
            self._apply_holdout(holdout_range)

        self._current_start_entry = self.start_entry
        self._current_stop_entry = self.start_entry + self.chunk_size

        if self._current_stop_entry > self.stop_entry:
            self._current_stop_entry = self.stop_entry

    def close(self) -> None:
        self.handle.close()

    def _apply_holdout(self, holdout_range: tuple[float, float]) -> None:
        total = self.stop_entry - self.start_entry

        lower, upper = holdout_range

        holdout_start_entry = self.start_entry + int(lower * total)
        holdout_stop_entry = self.start_entry + int(upper * total)

        self.start_entry, self.stop_entry = holdout_start_entry, holdout_stop_entry

    def _make_report(self) -> dict[str, Any]:
        return {
            "file": self.file,
            "dataset_name": self.dataset_name,
            "chunk_size": self.chunk_size,
            "start": self._current_start_entry,
            "stop": self._current_stop_entry,
        }

    def __iter__(self) -> Hdf5Iterator:
        return self

    def __next__(self) -> tuple[np.ndarray, dict[str, Any]]:
        if self._current_start_entry >= self.stop_entry:
            raise StopIteration

        dataset = self.handle[self.dataset_name]
        arrays = dataset[self._current_start_entry : self._current_stop_entry]

        if self.shuffle:
            np.random.shuffle(arrays)

        self._current_start_entry = self._current_stop_entry
        self._current_stop_entry = min(self._current_stop_entry + self.chunk_size, self.stop_entry)

        reports = self._make_report()

        return arrays, reports


class Hdf5IteratorDfMaker:
    def __init__(
        self,
        name: str,
        hdf5_files_metadata: dict[str, dict[str, Any]],
        num_workers: int,
        shape: tuple[int, int],
        chunk_size: int | None = None,
        shuffle: bool = False,
        holdout_range: tuple[float, float] | None = None,
    ) -> None:
        self.name = name
        self.hdf5_files_metadata = hdf5_files_metadata
        self.num_workers = num_workers
        self.shape = shape
        self.chunk_size = chunk_size
        self.shuffle = shuffle
        self.holdout_range = holdout_range

        self.total_num_entries = shape[0]
        self.all_num_entries_dct: dict[str, int] = {}

    def _log_info(self) -> None:
        all_hdf5_files = list(self.hdf5_files_metadata.keys())
        hdf5_files = set([f.split(":")[0] for f in all_hdf5_files])
        hdf5_datasets = set([f.split(":")[1] for f in all_hdf5_files])

        total_files_size = sum([get_file_size(file) for file in hdf5_files])

        info_str = "\n" + 15 * "=" + " info " + 15 * "="
        info_str += f"\nName: {self.name}\n"
        info_str += f"Number of hdf5 files: {len(hdf5_files)}\n"
        info_str += f"Number of datasets: {len(hdf5_datasets)}\n"
        info_str += f"Total size: {total_files_size:.3f} GB\n"
        info_str += f"Total number of entries: {self.total_num_entries}\n"
        info_str += 36 * "="

        logging.info(info_str)

    def _make_iterator(self, hdf5_file: str, entry_start: int, entry_stop: int) -> Hdf5Iterator:
        return Hdf5Iterator(
            hdf5_file,
            self.chunk_size,
            entry_start,
            entry_stop,
            shuffle=self.shuffle,
            holdout_range=self.holdout_range,
        )

    def _split(self) -> list[dict[str, list[int]]]:
        self._log_info()

        # how many entries each worker will process
        splits = [self.total_num_entries // self.num_workers] * self.num_workers
        splits[-1] += self.total_num_entries % self.num_workers

        self.all_num_entries_dct = {file: metadata["shape"][0] for file, metadata in self.hdf5_files_metadata.items()}
        num_entries_dct = copy.deepcopy(self.all_num_entries_dct)

        # keep track of the start and stop entries for each root file
        hdf5_files_start_dct: dict[str, int] = {file: 0 for file in self.hdf5_files_metadata.keys()}

        result: list[dict[str, list[int]]] = [{} for _ in range(len(splits))]

        done = []
        for i, split in enumerate(splits):

            total = 0
            for hdf5_file, num_entries in num_entries_dct.items():
                if hdf5_file in done:
                    continue

                start_entry = hdf5_files_start_dct[hdf5_file]

                total += num_entries

                if total <= split:
                    result[i][hdf5_file] = [start_entry, self.all_num_entries_dct[hdf5_file]]
                    done.append(hdf5_file)

                    if total == split:
                        break
                    else:
                        continue

                if total > split:
                    delta = num_entries - (total - split)
                    result[i][hdf5_file] = [start_entry, start_entry + delta]
                    hdf5_files_start_dct[hdf5_file] += delta
                    num_entries_dct[hdf5_file] -= delta
                    break

        return result

    def make(self) -> pd.DataFrame:
        split_result = self._split()

        worker_df: dict[str, list] = {
            "worker_id": [],
            "file": [],
            "start": [],
            "stop": [],
            "chunk_size": [],
            "holdout_range": [],
            "shuffle": [],
        }

        check_total = 0
        for i, result_dct in enumerate(split_result):
            for hdf5_file, start_stop in result_dct.items():
                entry_start, entry_stop = start_stop
                check_total += entry_stop - entry_start

                worker_df["worker_id"].append(i)
                worker_df["file"].append(hdf5_file)
                worker_df["start"].append(entry_start)
                worker_df["stop"].append(entry_stop)
                worker_df["chunk_size"].append(self.chunk_size)
                worker_df["holdout_range"].append(self.holdout_range)
                worker_df["shuffle"].append(self.shuffle)

        if check_total != self.total_num_entries:
            raise ValueError("Total number of entries does not match.")

        return pd.DataFrame(worker_df)


class Hdf5LoaderIterator:
    def __init__(
        self,
        name: str,
        iterators_df: pd.DataFrame,
        worker_id: int,
        processors: list[Callable[[ArrayLike, dict], tuple[ArrayLike, dict]]] | ProcessorsGraph | None = None,
        hdf5_files_desc_dct: dict[str, dict[str, Any]] | None = None,
    ) -> None:
        self.name = name
        self.iterators_df = iterators_df
        self.worker_id = worker_id
        self.processors = processors
        self.hdf5_files_desc_dct = hdf5_files_desc_dct

        self.current_df_idx, self.current_iterator_idx = 0, 0

    def _make_hdf5_iterator(self, df: pd.Series) -> Hdf5Iterator:
        iterator = Hdf5Iterator(
            df["file"],
            chunk_size=df["chunk_size"],
            start_entry=df["start"],
            stop_entry=df["stop"],
            shuffle=df["shuffle"],
            holdout_range=df["holdout_range"],
        )

        return iterator

    def _iterate_df(self) -> None:
        df = self.iterators_df.iloc[self.current_iterator_idx]
        self.iterator = self._make_hdf5_iterator(df)
        self.current_df_idx += 1

    def _run_processors(self, arrays: ArrayLike, reports: dict) -> tuple[ArrayLike, dict] | dict[str, Processor]:
        if self.processors is None:
            return arrays, reports
        elif type(self.processors) is list:
            for proc in self.processors:
                arrays, reports = proc(arrays, reports)
            return arrays, reports
        elif type(self.processors) is ProcessorsGraph:
            processors = self.processors.fit(arrays, reports)
            return processors
        else:
            raise ValueError(f"Processors {self.processors} is not a valid type.")

    def _make_report(self, reports: Any) -> dict:
        reports = {"name": self.name, "worker_id": self.worker_id} | reports

        if self.hdf5_files_desc_dct is not None:
            file_name = os.path.basename(reports["file"])
            reports = reports | self.hdf5_files_desc_dct[file_name]

        return reports

    def __iter__(self) -> Hdf5LoaderIterator:
        return self

    def __next__(self) -> tuple[ArrayLike, dict] | dict[str, Processor]:
        try:
            if self.current_df_idx == self.current_iterator_idx:
                self._iterate_df()

            arrays, reports = next(self.iterator)

        except StopIteration:
            self.iterator.close()
            self.current_iterator_idx += 1

            if self.current_iterator_idx == len(self.iterators_df):
                raise StopIteration

            if self.current_df_idx == self.current_iterator_idx:
                self._iterate_df()

            arrays, reports = next(self.iterator)

        reports = self._make_report(reports)

        processors_return = self._run_processors(arrays, reports)

        return processors_return


class Hdf5IterableDataset(IterableDataset):
    def __init__(
        self,
        name: str,
        files: list[str],
        dataset_names: list[str],
        num_workers: int,
        chunk_size: int | None = None,
        use_piles: bool = False,
        shuffle: bool = False,
        holdout_range: tuple[float, float] | None = None,
        processors: list[Callable[[ArrayLike, dict], tuple[ArrayLike, dict]]] | ProcessorsGraph | None = None,
        hdf5_files_desc_dct: dict[str, dict[str, Any]] | None = None,
    ) -> None:
        super().__init__()
        self.name = name
        self.files = files
        self.dataset_names = dataset_names
        self.num_workers = num_workers
        self.chunk_size = chunk_size
        self.use_piles = use_piles
        self.shuffle = shuffle
        self.holdout_range = holdout_range
        self.hdf5_files_desc_dct = hdf5_files_desc_dct

        if self.use_piles is False and self.chunk_size is None:
            raise ValueError("Chunk size must be provided if not using piles!")

        self.processors = processors
        if isinstance(self.processors, ProcessorsGraph):
            self.processors.copy_processors = True

        self.metadata: dict[str, dict[str, Any]] = {}

        if self.use_piles:
            self._setup_piles()
        else:
            self._setup()

        self.shape = self._get_total_shape()

        self.worker_iterators_df = self._get_df_iterators()

    def _setup(self) -> None:
        for file, dataset_name in product(self.files, self.dataset_names):
            if dataset_name not in self._get_keys(file):
                logging.warning(f"Dataset {dataset_name} not found in {file}. Skipping!")
                continue

            metadata_key = f"{file}:{dataset_name}"

            self.metadata[metadata_key] = {"shape": None}

            shape = self._get_shape(file, dataset_name)
            self.metadata[metadata_key]["shape"] = shape

    def _setup_piles(self) -> None:
        piles_metadata: dict[str, dict[str, Any]] = {}

        for file, dataset_name in product(self.files, self.dataset_names):
            if dataset_name not in self._get_keys(file):
                logging.warning(f"Dataset {dataset_name} not found in {file}. Skipping!")
                continue

            if file not in piles_metadata:
                piles_metadata[file] = {"piles_lst": [], "piles_shapes": []}

            piles_lst = self._get_piles_metadata(file)["piles"][dataset_name]
            piles_metadata[file]["piles_lst"] += piles_lst

            piles_shapes = self._get_piles_shape(file, piles_lst)
            piles_metadata[file]["piles_shapes"] += piles_shapes

        for file, metadata in piles_metadata.items():
            for pile, shape in zip(metadata["piles_lst"], metadata["piles_shapes"]):
                metadata_key = f"{file}:{pile}"
                self.metadata[metadata_key] = {"shape": shape}

    @staticmethod
    def _get_keys(file_path: str) -> list[str]:
        with h5py.File(file_path, "r") as f:
            keys = list(f.keys())

        return keys

    @staticmethod
    def _get_piles_metadata(file_path: str) -> dict[str, Any]:
        with h5py.File(file_path, "r") as f:
            metadata = json.loads(f["metadata"][()])

        return metadata

    @staticmethod
    def _get_shape(file_path: str, dataset_name: str) -> tuple[int, int]:
        with h5py.File(file_path, "r") as f:
            shape = f[dataset_name].shape

        return shape

    @staticmethod
    def _get_piles_shape(file_path: str, piles_lst: str) -> list[tuple[int, int]]:
        with h5py.File(file_path, "r") as f:
            shape = [f[pile].shape for pile in piles_lst]

        return shape

    def _get_total_shape(self) -> tuple[int, int]:
        shapes_0, shapes_1 = [], []

        for shape in self.metadata.values():
            shapes_0.append(shape["shape"][0])
            shapes_1.append(shape["shape"][1])

        if len(set(shapes_1)) > 1:
            raise ValueError("All datasets must have the same number of columns")

        return sum(shapes_0), shapes_1[0]

    def _get_df_iterators(self) -> pd.DataFrame:
        return Hdf5IteratorDfMaker(
            self.name,
            self.metadata,
            self.num_workers,
            self.shape,
            self.chunk_size,
            self.shuffle,
            self.holdout_range,
        ).make()

    def __iter__(self) -> Hdf5LoaderIterator:
        worker_info = torch.utils.data.get_worker_info()

        if worker_info is None:
            worker_id = 0
        else:
            worker_id = worker_info.id

        iterators_df = self.worker_iterators_df[self.worker_iterators_df["worker_id"] == worker_id].copy()

        return Hdf5LoaderIterator(
            self.name,
            iterators_df,
            worker_id,
            self.processors,
            self.hdf5_files_desc_dct,
        )


def default_collate_fn(batch: list[Any]) -> list[Any]:
    return batch


def get_hdf5_dataloader(
    name: str,
    files: str | list[str],
    dataset_names: str | list[str],
    num_workers: int,
    chunk_size: int | None = None,
    use_piles: bool = False,
    shuffle: bool = False,
    holdout_range: tuple[float, float] | None = None,
    hdf5_files_desc_dct: dict[str, dict[str, Any]] | None = None,
    processors: list[Callable[[ArrayLike, dict], tuple[ArrayLike, dict]]] | ProcessorsGraph | None = None,
    dataloader_kwargs: dict[str, Any] | None = None,
) -> tuple[DataLoader, int]:

    if multiprocessing.get_start_method() == "fork" and num_workers > 0:
        logging.debug("Using 'fork' start method. Consider using 'spawn' or 'forkserver'.")

    if num_workers == -1:
        num_workers = multiprocessing.cpu_count()

    if type(files) is str:
        files = [files]
    elif type(files) is not list:
        raise ValueError("files must be a string or a list of strings!")

    if type(dataset_names) is str:
        dataset_names = [dataset_names]
    elif type(dataset_names) is not list:
        raise ValueError("dataset_names must be a string or a list of strings!")

    if dataloader_kwargs is None:
        dataloader_kwargs = {}

    hdf5_dataset = Hdf5IterableDataset(
        name,
        files,
        dataset_names,
        num_workers=num_workers if num_workers > 0 else 1,
        chunk_size=chunk_size,
        use_piles=use_piles,
        shuffle=shuffle,
        holdout_range=holdout_range,
        processors=processors,
        hdf5_files_desc_dct=hdf5_files_desc_dct,
    )

    hdf5_dataloader = DataLoader(
        hdf5_dataset,
        batch_size=None,
        num_workers=num_workers,
        collate_fn=default_collate_fn,
        **dataloader_kwargs,
    )

    return hdf5_dataloader, hdf5_dataset.shape[0]
