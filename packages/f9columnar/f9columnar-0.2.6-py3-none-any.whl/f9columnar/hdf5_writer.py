from __future__ import annotations

import copy
import json
import logging
import time
from abc import abstractmethod
from collections import deque
from typing import Any

import awkward as ak
import h5py
import numpy as np
from rich.progress import track

from f9columnar.processors import Postprocessor, Processor
from f9columnar.utils.loggers import timeit


class ArraysHdf5Writer(Postprocessor):
    def __init__(self, file_path: str, dataset_names: str | list[str] | None = None, name: str = "HDF5Writer") -> None:
        """Class for HDF5 data writer postprocessors that write awkward arrays to HDF5 file.

        Parameters
        ----------
        file_path : str
            Path to the created HDF5 file.
        dataset_names : str | list[str] | None, optional
            Names of the datasets to be created. Can be dir/subdir/.../dataset_name.
        name : str, optional
            Name of the processor.

        Other Parameters
        ----------------
        shape, chunks, maxshape, dtype, compression, compression_opts
            See [1].

        References
        ----------
        [1] - https://docs.h5py.org/en/stable/high/group.html#h5py.Group.create_dataset
        [2] - https://docs.h5py.org/en/stable/high/dataset.html
        [3] - https://pythonforthelab.com/blog/how-to-use-hdf5-files-in-python/

        """
        super().__init__(name)
        self.file_path = file_path

        if type(dataset_names) is str:
            self.dataset_names = [dataset_names]
        elif type(dataset_names) is list:
            self.dataset_names = dataset_names
        else:
            self.dataset_names = []

        self._current_idx = 0
        self._current_shape: int | None = None

    def create_datasets(
        self,
        mode: str = "w",
        dataset_names: list[str] | None = None,
        shape: tuple[int, int] | None = None,
        chunks: bool = False,
        maxshape: tuple[int | None, int] | None = None,
        dtype: str = "float32",
        compression: str = "lzf",
        compression_opts: int | None = None,
    ) -> None:
        if mode not in ["w", "a"]:
            raise ValueError("Mode must be 'w' or 'a'!")

        if maxshape is not None and shape is None:
            raise ValueError("Shape must be provided if maxshape is provided!")

        if chunks is None and maxshape or compression:
            logging.info("Auto-chunking is enabled by default, if you use compression or maxshape.")
            chunks = True

        if dataset_names is None:
            dataset_names = self.dataset_names

            if len(dataset_names) == 0:
                raise ValueError("No dataset names provided!")

        with h5py.File(self.file_path, mode) as f:
            for dataset_name in dataset_names:
                dataset_name_split = dataset_name.split("/")

                f_obj = f
                for i, group in enumerate(dataset_name_split):
                    if i == len(dataset_name_split) - 1:
                        f_obj.create_dataset(
                            group,
                            shape=shape,
                            chunks=chunks,
                            maxshape=maxshape,
                            dtype=dtype,
                            compression=compression,
                            compression_opts=compression_opts,
                        )
                    elif i == 0:
                        if group not in f_obj:
                            g = f.create_group(group)
                            f_obj = g
                        else:
                            f_obj = f_obj[group]
                    else:
                        g = g.create_group(group)
                        f_obj = g

    def add_data(
        self,
        data: np.ndarray,
        dataset_name: str,
        idx: int | tuple[int, int],
        resize: tuple | None = None,
    ) -> None:
        if type(idx) is tuple and len(idx) > 2:
            raise ValueError("Only support 2D data!")

        with h5py.File(self.file_path, "a") as f:
            dataset = f[dataset_name]

            if resize:
                dataset.resize(resize)

            if type(idx) is int:
                dataset[idx] = data
            elif type(idx) is tuple:
                dataset[idx[0] : idx[1]] = data
            else:
                raise TypeError("idx must be a tuple or an integer!")

    def add_metadata(self, metadata_dct: dict[str, Any], group_name: str | None = None) -> None:
        with h5py.File(self.file_path, "a") as f:
            if group_name is not None:
                group = f[group_name]
            else:
                group = f

            group.create_dataset("metadata", data=json.dumps(metadata_dct))

    def get_metadata(self, group_name: str | None = None) -> dict[str, Any]:
        if group_name is None:
            group_name = "metadata"
        else:
            group_name = f"{group_name}/metadata"

        with h5py.File(self.file_path, "r") as f:
            metadata = json.loads(f[group_name][()])

        return metadata

    def get_keys(self) -> list[str]:
        with h5py.File(self.file_path, "r") as f:
            keys = list(f.keys())

        return keys

    def get_handle(self, mode: str = "r") -> h5py.File:
        return h5py.File(self.file_path, mode)

    def write_arrays(
        self,
        arrays: ak.Array,
        dataset_name: str,
        column_names: list[str],
        chunk_shape: int = 1000,
    ) -> None:
        if self._current_shape is None:
            self._current_shape = chunk_shape

        save_arrays = []

        for column_name in column_names:
            if column_name not in arrays.fields:
                raise RuntimeError(f"Column {column_name} not found in arrays!")

            column = ak.to_numpy(arrays[column_name])
            column = column[:, None]
            save_arrays.append(column)

        save_arrays = np.concatenate(save_arrays, axis=1)

        array_chunks = len(save_arrays) // chunk_shape + 1
        chunk_save_arrays = np.array_split(save_arrays, array_chunks)

        for chunk_array in chunk_save_arrays:
            n_chunk = len(chunk_array)
            start_idx, stop_idx = self._current_idx, self._current_idx + n_chunk

            self._current_idx = stop_idx

            if self._current_idx > self._current_shape:
                resize = (stop_idx, chunk_array.shape[1])
                self._current_shape = stop_idx
            else:
                resize = None

            self.add_data(chunk_array, dataset_name, idx=(start_idx, stop_idx), resize=resize)

    @abstractmethod
    def run(self, processors: dict[str, Processor], *args: Any, **kwargs: Any):
        pass


class ArraysHdf5PileWriter(ArraysHdf5Writer):
    def __init__(
        self,
        file_path: str,
        n_piles: int,
        pile_assignment: str = "random",
        dataset_names: str | list[str] | None = None,
        name: str = "HDF5Writer",
    ) -> None:
        """Implementation of ArraysHDF5Writer using piles. A pile is a separate dataset in the HDF5 file. Each chunk of
        data is saved to a random pile. This allows for processing large datasets that do not fit into memory and allows
        for shuffling the data during the writing process and reading process.

        Parameters
        ----------
        file_path : str
            Path to the created HDF5 file.
        n_piles : int
            Number of piles to split the data into.
        pile_assignment : str, optional
            Method of assigning data to piles. Can be 'deque' or 'random'.
        dataset_names : str | list[str] | None, optional
            Names of the datasets to be created. Can be dir/subdir/.../dataset_name.
        name : str, optional
            Name of the processor.

        Warning
        -------
        There is a chance that some piles will be missed in case of a small dataset. This is seen as piles of zeros in
        the HDF5 file. This can be fixed by setting the number of piles to an appropriate value.

        TODO: every dataset name should have its own deque to have better pile assignment coverage.

        References
        ----------
        [1] - https://blog.janestreet.com/how-to-shuffle-a-big-dataset/

        """
        super().__init__(file_path, dataset_names, name)
        self.n_piles = n_piles

        if pile_assignment not in ["deque", "random"]:
            raise ValueError("Pile assignment must be 'deque' or 'random'!")

        self.pile_assignment = pile_assignment

        if self.pile_assignment == "deque":
            self.pile_deque = deque(range(self.n_piles))

        # list of all datasets, mapping from each dataset name to a list of corresponding pile names
        self.pile_datasets_lst, self.pile_datasets_dct = self.get_pile_dataset_names()
        # mapping from each dataset name to a dictionary of its pile names and their current index and shape
        self.piles_info_dct = self.get_piles_info(start_dct={"current_idx": 0, "current_shape": None})

        self.current_dataset_name: str
        self.current_pile_name: str

    def get_pile_dataset_names(self) -> tuple[list[str], dict[str, list[str]]]:
        pile_datasets_lst, pile_datasets_dct = [], {}

        for dataset_name in self.dataset_names:
            piles = [f"{dataset_name}/p{i}" for i in range(self.n_piles)]

            pile_datasets_lst += piles
            pile_datasets_dct[dataset_name] = piles

        return pile_datasets_lst, pile_datasets_dct

    def get_piles_info(self, start_dct) -> dict[str, dict[str, dict[str, Any]]]:
        piles_info_dct = {}

        for dataset_name, pile_names in self.pile_datasets_dct.items():
            info_dct = {}

            for pile_name in pile_names:
                info_dct[pile_name] = copy.deepcopy(start_dct)

            piles_info_dct[dataset_name] = info_dct

        return piles_info_dct

    def set_current_pile_idx(self, value: int) -> ArraysHdf5PileWriter:
        self.piles_info_dct[self.current_dataset_name][self.current_pile_name]["current_idx"] = value
        return self

    def set_current_pile_shape(self, value: int) -> ArraysHdf5PileWriter:
        self.piles_info_dct[self.current_dataset_name][self.current_pile_name]["current_shape"] = value
        return self

    @property
    def current_pile_idx(self) -> int:
        return self.piles_info_dct[self.current_dataset_name][self.current_pile_name]["current_idx"]

    @property
    def current_pile_shape(self) -> int:
        return self.piles_info_dct[self.current_dataset_name][self.current_pile_name]["current_shape"]

    def write_arrays(
        self,
        arrays: ak.Array,
        dataset_name: str,
        column_names: list[str],
        chunk_shape: int = 1000,
    ) -> None:
        self.current_dataset_name = dataset_name

        save_arrays = []

        for column_name in column_names:
            if column_name not in arrays.fields:
                raise RuntimeError(f"Column {column_name} not found in arrays!")

            column = ak.to_numpy(arrays[column_name])
            column = column[:, None]
            save_arrays.append(column)

        save_arrays = np.concatenate(save_arrays, axis=1)

        array_chunks = len(save_arrays) // chunk_shape + 1
        chunk_save_arrays = np.array_split(save_arrays, array_chunks)

        for chunk_array in chunk_save_arrays:
            if self.pile_assignment == "deque":
                pile_idx = self.pile_deque[0]
                self.pile_deque.rotate(-1)
            else:
                pile_idx = np.random.choice(self.n_piles)

            self.current_pile_name = self.pile_datasets_dct[dataset_name][pile_idx]

            if self.current_pile_shape is None:
                self.set_current_pile_shape(chunk_shape)

            n_chunk = len(chunk_array)

            start_idx = self.current_pile_idx
            stop_idx = start_idx + n_chunk

            self.set_current_pile_idx(stop_idx)

            if self.current_pile_idx > self.current_pile_shape:
                resize = (stop_idx, chunk_array.shape[1])
                self.set_current_pile_shape(stop_idx)
            else:
                resize = None

            self.add_data(chunk_array, self.current_pile_name, idx=(start_idx, stop_idx), resize=resize)

    @abstractmethod
    def run(self, processors: dict[str, Processor], *args: Any, **kwargs: Any):
        pass


class DatasetHdf5Writer(ArraysHdf5Writer):
    def __init__(
        self,
        file_path: str,
        dataset_name: str,
        column_names: list[str],
        save_node: str = "output",
        chunk_shape: int = 1000,
        name: str = "datasetHDF5Writer",
        **hdf5_kwargs: Any,
    ) -> None:
        super().__init__(file_path, dataset_names=dataset_name, name=name)
        self.chunk_shape = chunk_shape
        self.column_names = column_names
        self.save_node = save_node

        self.create_datasets(
            shape=(chunk_shape, len(column_names)),
            maxshape=(None, len(column_names)),
            **hdf5_kwargs,
        )
        self.add_metadata({"columns": self.column_names})

    def run(self, processors: dict[str, Processor]) -> dict[str, dict[str, Processor]]:
        arrays_processor = processors[self.save_node]

        if hasattr(arrays_processor, "arrays"):
            arrays = arrays_processor.arrays
        else:
            raise AttributeError("Arrays attribute not found in the processor!")

        self.write_arrays(arrays, self.dataset_names[0], self.column_names, self.chunk_shape)

        return {"processors": processors}


class DatasetHdf5PileWriter(ArraysHdf5PileWriter):
    def __init__(
        self,
        file_path: str,
        dataset_name: str,
        n_piles: int,
        column_names: list[str],
        pile_assignment: str = "random",
        save_node: str = "output",
        chunk_shape: int = 1000,
        name: str = "datasetHDF5Writer",
        **hdf5_kwargs: Any,
    ) -> None:
        super().__init__(file_path, n_piles, pile_assignment, dataset_name, name)
        self.chunk_shape = chunk_shape
        self.column_names = column_names
        self.save_node = save_node

        self.create_datasets(
            dataset_names=self.pile_datasets_lst,
            shape=(chunk_shape, len(column_names)),
            maxshape=(None, len(column_names)),
            **hdf5_kwargs,
        )
        self.add_metadata({"columns": self.column_names, "piles": self.pile_datasets_dct})

    def run(self, processors: dict[str, Processor]) -> dict[str, dict[str, Processor]]:
        arrays_processor = processors[self.save_node]

        if hasattr(arrays_processor, "arrays"):
            arrays = arrays_processor.arrays
        else:
            raise AttributeError("Arrays attribute not found in the processor!")

        self.write_arrays(arrays, self.dataset_names[0], self.column_names, self.chunk_shape)

        return {"processors": processors}


class NtupleHdf5Writer(ArraysHdf5Writer):
    def __init__(
        self,
        file_path: str,
        mc_column_names: list[str],
        data_column_names: list[str] | None = None,
        save_node: str = "output",
        chunk_shape: int = 1000,
        write_mc: bool = True,
        write_data: bool = True,
        name: str = "datasetHDF5Writer",
        dataset_names: list[str] | None = None,
        **hdf5_kwargs: Any,
    ) -> None:

        if dataset_names is None:
            dataset_names = ["mc", "data"]

        if len(dataset_names) != 2:
            raise ValueError("Dataset names must be a list of two strings!")

        super().__init__(file_path, dataset_names=dataset_names, name=name)
        self.save_node = save_node
        self.chunk_shape = chunk_shape

        if write_data is False and write_mc is False:
            raise ValueError("Both write_data and write_mc cannot be False!")

        self.write_data, self.write_mc = write_data, write_mc

        self.mc_column_names = mc_column_names

        if data_column_names is None:
            logging.info("Data column names not provided, using MC column names.")
            self.data_column_names = mc_column_names
        else:
            self.data_column_names = data_column_names

        metadata = {}
        mc_group, data_group = self.dataset_names[0], self.dataset_names[1]

        if write_mc:
            self.create_datasets(
                dataset_names=[mc_group],
                shape=(self.chunk_shape, len(self.mc_column_names)),
                maxshape=(None, len(self.mc_column_names)),
                **hdf5_kwargs,
            )
            metadata[f"{mc_group}_columns"] = self.mc_column_names

        if write_data:
            self.create_datasets(
                mode="a" if self.write_mc else "w",
                dataset_names=[data_group],
                shape=(self.chunk_shape, len(self.data_column_names)),
                maxshape=(None, len(self.data_column_names)),
                **hdf5_kwargs,
            )
            metadata[f"{data_group}_columns"] = self.data_column_names

        self.add_metadata(metadata)

        self._current_mc_idx, self._current_data_idx = 0, 0
        self._current_mc_shape, self._current_data_shape = None, None

    def run(self, processors: dict[str, Processor]) -> dict[str, dict[str, Processor]]:
        arrays_processor = processors[self.save_node]

        if hasattr(arrays_processor, "arrays"):
            arrays = arrays_processor.arrays
        else:
            raise AttributeError("Arrays attribute not found in the processor!")

        if self.is_data and self.write_data:
            self._current_idx, self._current_shape = self._current_mc_idx, self._current_mc_shape
            self.write_arrays(arrays, self.dataset_names[1], self.data_column_names, self.chunk_shape)
            self._current_mc_idx, self._current_mc_shape = self._current_idx, self._current_shape

        if not self.is_data and self.write_mc:
            self._current_idx, self._current_shape = self._current_data_idx, self._current_data_shape
            self.write_arrays(arrays, self.dataset_names[0], self.mc_column_names, self.chunk_shape)
            self._current_data_idx, self._current_data_shape = self._current_idx, self._current_shape

        return {"processors": processors}


class NtupleHdf5PileWriter(ArraysHdf5PileWriter):
    def __init__(
        self,
        file_path: str,
        n_piles: int,
        mc_column_names: list[str],
        data_column_names: list[str] | None = None,
        pile_assignment: str = "random",
        save_node: str = "output",
        chunk_shape: int = 1000,
        write_mc: bool = True,
        write_data: bool = True,
        name: str = "datasetHDF5Writer",
        dataset_names_map: dict[str, str] | None = None,
        **hdf5_kwargs: Any,
    ) -> None:

        if dataset_names_map is None:
            dataset_names = ["mc", "data"]
        else:
            dataset_names = [dataset_names_map["mc"], dataset_names_map["data"]]

        if len(dataset_names) != 2:
            raise ValueError("Dataset names must be a list of two strings!")

        super().__init__(file_path, n_piles, pile_assignment, dataset_names=dataset_names, name=name)
        self.save_node = save_node
        self.chunk_shape = chunk_shape

        if write_data is False and write_mc is False:
            raise ValueError("Both write_data and write_mc cannot be False!")

        self.write_data, self.write_mc = write_data, write_mc

        self.mc_column_names = mc_column_names

        if data_column_names is None:
            logging.info("Data column names not provided, using MC column names.")
            self.data_column_names = mc_column_names
        else:
            self.data_column_names = data_column_names

        metadata: dict[str, Any] = {}
        mc_group, data_group = self.dataset_names[0], self.dataset_names[1]

        if write_mc:
            self.create_datasets(
                dataset_names=self.pile_datasets_dct[mc_group],
                shape=(self.chunk_shape, len(self.mc_column_names)),
                maxshape=(None, len(self.mc_column_names)),
                **hdf5_kwargs,
            )
            metadata[f"{mc_group}_columns"] = self.mc_column_names

        if write_data:
            self.create_datasets(
                mode="a" if self.write_mc else "w",
                dataset_names=self.pile_datasets_dct[data_group],
                shape=(self.chunk_shape, len(self.data_column_names)),
                maxshape=(None, len(self.data_column_names)),
                **hdf5_kwargs,
            )
            metadata[f"{data_group}_columns"] = self.data_column_names

        metadata["piles"] = self.pile_datasets_dct

        self.add_metadata(metadata)

    def run(self, processors: dict[str, Processor]) -> dict[str, dict[str, Processor]]:
        arrays_processor = processors[self.save_node]

        if hasattr(arrays_processor, "arrays"):
            arrays = arrays_processor.arrays
        else:
            raise AttributeError("Arrays attribute not found in the processor!")

        if self.is_data and self.write_data:
            self.write_arrays(arrays, self.dataset_names[1], self.data_column_names, self.chunk_shape)

        if not self.is_data and self.write_mc:
            self.write_arrays(arrays, self.dataset_names[0], self.mc_column_names, self.chunk_shape)

        return {"processors": processors}


class PileShuffler:
    def __init__(self, file_path: str, dataset_names: str | list[str] | None = None) -> None:
        self.file_path = file_path

        if type(dataset_names) is str:
            self.dataset_names = [dataset_names]
        elif type(dataset_names) is list:
            self.dataset_names = dataset_names
        else:
            self.dataset_names = []

        self.pile_datasets = self._get_pile_datasets()

    def _get_pile_datasets(self) -> dict[str, list[str]]:
        pile_datasets = {}

        with h5py.File(self.file_path, "r") as f:
            for dataset_name in self.dataset_names:
                if dataset_name not in f:
                    raise ValueError(f"Dataset {dataset_name} not found in the file!")

                pile_datasets[dataset_name] = list(f[dataset_name].keys())

        return pile_datasets

    def _shuffle_dataset_pile(self, dataset_name: str, pile: str) -> float:
        start_time = time.time()

        with h5py.File(self.file_path, "r+") as f:
            data = f[f"{dataset_name}/{pile}"][:]
            np.random.shuffle(data)
            f[f"{dataset_name}/{pile}"][:] = data

        return time.time() - start_time

    @timeit("s")
    def shuffle(self) -> list[float]:
        shuffle_args = []

        for dataset_name, piles in self.pile_datasets.items():
            for pile in piles:
                shuffle_args.append((dataset_name, pile))

        results = []
        for shuffle_arg in track(shuffle_args, description="Shuffling piles...", total=len(shuffle_args)):
            result = self._shuffle_dataset_pile(*shuffle_arg)
            results.append(result)

        logging.info(f"Shuffled {len(results)} piles!")

        return results
