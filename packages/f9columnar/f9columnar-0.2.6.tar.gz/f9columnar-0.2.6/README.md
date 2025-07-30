# F9 Columnar

A lightweight Python package for batch processing of ROOT and HDF5 event data.

### Project description

This package is designed for efficient handling of large datasets. Built on PyTorch, Awkward Array, and Uproot, it utilizes PyTorch's DataLoader with an IterableDataset to enable parallel processing. It implements a columnar event loop, returning batches of events in a format compatible with standard PyTorch training loops over multiple epochs.

Optimized for machine learning applications, the package provides `RootDataLoader` and `Hdf5DataLoader` classes for data loading from ROOT and HDF5 files. Additionally, it supports parallel data processing through a modular pipeline of processor classes, allowing users to chain operations for complex computations and histogramming.

##  Setup

### Install with PyTorch GPU

```shell
pip install f9columnar[torch]
```

### Install with PyTorch CPU (recommended)

```shell
pip install f9columnar
pip install torch --index-url https://download.pytorch.org/whl/cpu
```

### Install without PyTorch

```shell
pip install f9columnar
```

## Getting started example

The following example demonstrates how to load data from multiple ROOT files, apply a simple filter to select two branches, define variables, apply a cut, and create a histogram.

```python
from f9columnar.root_dataloader import get_root_dataloader

def filter_branch(branch):
    # select only these two branches
    return branch == "tau_p4" or branch == "lephad_p4"

# root_dataloader is an instance of a torch DataLoader that uses an IterableDataset
root_dataloader, total = get_root_dataloader(
    name="data", # name identifier
    files=ntuple_files, # root files
    key="NOMINAL", # root file tree name
    step_size=10**5, # number of events per array batch to read into memory
    num_workers=12, # number of workers for parallel processing
    processors=None, # arbitrary calculations on arrays
    filter_name=filter_branch, # filter branches
)

# loop over batches of events from .root file(s), each batch is an awkward array
for events in root_dataloader:
    arrays, report = events
    # ... do something with the arrays
```

Calculations on arrays within worker processes can be performed using a `Processor`. Multiple processors can be linked together in a `ProcessorsGraph`, forming a directed acyclic graph (DAG). These processors are applied to arrays in the sequence determined by the DAG’s topological order.

Each worker executes the same processor graph on batches of event data and returns the results to the event loop once processing is complete. In the example above, 12 (`num_workers`) processor graphs would be running in parallel, each handling small batches of events. Below is an example demonstrating how to calculate the tau visible mass and apply a cut to this variable.

```python
from f9columnar.processors import ProcessorsGraph, CheckpointProcessor
from f9columnar.object_collections import Variable, VariableCollection, Cut, CutCollection
from f9columnar.histograms import HistogramProcessor

class VisibleMass(Variable): # Variable is a Processor
    name = "vis_mass" # processor name
    branch_name = "lephad_p4" # name of the branch in the .root file

    def __init__(self):
        super().__init__()

    def run(self, arrays): # each processor must implement a run method
        lephad_p4 = arrays[self.branch_name] # branch_name is the name of the field in the ak array
        v = get_kinematics_vector(lephad_p4) # use vector with px, py, pz and E

        arrays["tau_vis_mass"] = v.m # add a new field to the arrays

        return {"arrays": arrays} # return the arrays (can also return None if no changes are made)

class CutVisibleMass(Cut): # Cut is a Processor
    name = "vis_mass_cut"
    branch_name = None # is not a branch in ntuples but was defined in the VisibleMass processor

    def __init__(self, cut_lower, cut_upper): # argumnets of the processor
        super().__init__()
        self.cut_lower = cut_lower
        self.cut_upper = cut_upper

    def run(self, arrays):
        mask = (arrays["tau_vis_mass"] > self.cut_lower) & (arrays["tau_vis_mass"] < self.cut_upper)
        arrays = arrays[mask] # apply the cut

        return {"arrays": arrays} # return must be a dictionary with key name for the argument of the next processor

class Histograms(HistogramProcessor):
    def __init__(self, name="histograms"):
        super().__init__(name)

        self.make_hist1d("tau_vis_mass", 20, 80.0, 110.0) # make a histogram with 20 bins from 80 to 110 GeV

    def run(self, arrays):
        return super().run(arrays) # auto fills histograms if array names match histogram names

var_collection = VariableCollection(VisibleMass, init=False) # will initialize later
cut_collection = CutCollection(CutVisibleMass, init=False)

collection = var_collection + cut_collection # add collections of objects together
branch_filter = collection.branch_name_filter # defines the branches that the processors depend on

graph = ProcessorsGraph() # graph has a fit method that gets called inside the root_dataloader

# add nodes to the graph
graph.add(
    CheckpointProcessor("input"), # input node
    var_collection["vis_mass"](), # initialize the processor
    cut_collection["vis_mass_cut"](cut_lower=90.0, cut_upper=100.0),
    CheckpointProcessor("output", save_arrays=True), # saves final arrays
    Histograms(),
)

# build a processor graph
graph.connect(
    [
        ("input", "vis_mass"),
        ("vis_mass", "vis_mass_cut"),
        ("vis_mass_cut", "output"),
        ("output", "histograms"),
    ]
)

# plot the graph
graph.draw("graph.pdf")

# ... pass into the root_dataloader with the processors argument (e.g. processors=graph)
# in this case the dataloader will return a fitted graph
for processed_graph in dataloader:
    histograms = processed_graph["histograms"].hists
    arrays = processed_graph["output"].arrays
    # ... do something with the histograms and arrays
```

A higher level of abstraction is also possible using the [`ColumnarEventLoop`](f9columnar/run.py) class. See benchmark [examples](benchmark/f9columnar_benchmark.py) for some more details.

## aCT

Basic job submitting to Slovenian grid is also possible using aCT. Currently it only supports Ntuple analysis data format from rucio (for [R21](https://gitlab.cern.ch/atlas-dch-seesaw-analyses/MultiLeptonAnalysis) and [R25](https://gitlab.cern.ch/atlas-dch-seesaw-analyses/EnhancedCPToolkit)).

### Installation

[ARC](https://doc.vega.izum.si/arc) Control Tower (aCT) is a system for submitting and managing payloads on ARC (and other) Computing Elements. It is used to submit jobs on sites in Slovenia. Install aCT client from the repository with the following command to the virtual environment (or with poetry):

```shell
pip install "git+https://github.com/ARCControlTower/aCT.git@test#subdirectory=src/act/client/aCT-client"
```

The command `act` is available in `PATH` as the virtual environment is activated. See the scripts in the [`submit`](f9columnar/submit/) directory for further details.

### Voms proxy setup

Note that it is recommended to be in `/atlas/si` group and make the proxy with it. Active it using (in a separate terminal):

```shell
setupATLAS
lsetup emi
voms-proxy-init --valid 96:0 --voms atlas:/atlas/si
```

To propagate the proxy to the system use

```shell
act proxy
```

At this point you are ready to use aCT.

## Examples

- [Mini-analysis](https://gitlab.cern.ch/jgavrano/columnar-seesaw)
- [Converting ROOT to HDF5](https://gitlab.cern.ch/atlas-dch-seesaw-analyses/SeeSawML/-/blob/main/seesaw/fakes/hdf5_converter.py?ref_type=heads)
- [HDF5 Dataloader for ML](https://gitlab.cern.ch/atlas-dch-seesaw-analyses/SeeSawML/-/blob/main/seesaw/fakes/hdf5_dataloader.py?ref_type=heads)
- [Histogramming](https://gitlab.cern.ch/atlas-dch-seesaw-analyses/SeeSawML/-/blob/main/seesaw/fakes/el_fake_hists.py?ref_type=heads)

## Development

### Development install

Use [poetry](https://python-poetry.org/) to install the required packages:

```shell
poetry config cache-dir $PWD
poetry config virtualenvs.in-project true
poetry install -E torch
```

Note: this environment should be duplicated for batch processing on dCache.

### Making a portable venv with conda

Make sure you have [Miniconda](https://docs.anaconda.com/miniconda/) installed:

```shell
mkdir miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda3/miniconda.sh
bash miniconda3/miniconda.sh -b -u -p miniconda3
rm -rf miniconda3/miniconda.sh
miniconda3/bin/conda init bash
```

`init` command will add some path variables to your `~/.bashrc` that you can delete when done.

To test conda install use:

```shell
conda -V
```

Next, make a virtual environment:

```shell
conda create -n batch_venv python=3.12.4
source activate batch_venv
```

Install the required packages:

```shell
pip install f9columnar
pip install torch --index-url https://download.pytorch.org/whl/cpu
```

In order to make this environment portable use [conda-pack](https://conda.github.io/conda-pack/):

```shell
conda install conda-pack
conda pack
conda deactivate
```

On remote machine unpack the environment:

```shell
tar -xzf batch_venv.tar.gz
source batch_venv/bin/activate
conda-unpack
```

### dCache

Basic instructions can be found [here](https://doc.sling.si/en/navodila/podatki/).

To upload the above described venv to dCache use:

```shell
arccp batch_venv.tar davs://dcache.sling.si:2880/atlas/jang/
```

where you can make your own directory with `arcmkdir`.

### lxplus venv setup

Log into lxplus:
```shell
ssh <name>@lxplus.cern.ch
```

Since we want custom python packages and installing on `afs` is not recommended, we will use `eos`:
```shell
cd /eos/user/j/jgavrano
```

Source an LCG release to use as base:
```shell
setupATLAS
lsetup "views LCG_105b x86_64-el9-gcc13-opt"
```

Setup `venv` and install required packages from `requirements`:
```shell
PYTHONUSERBASE=/eos/user/j/jgavrano/F9Columnar/ pip3 install --user --no-cache-dir -r requirements.txt
```

Test with libraries in `eos`:
```shell
PYTHONPATH=/eos/user/j/jgavrano/F9Columnar/lib/python3.9/site-packages/:$PYTHONPATH python3 <script_name>.py
```

Setup python with custom `venv`:
```shell
export PYTHONPATH=/eos/user/j/jgavrano/F9Columnar/lib/python3.9/site-packages/:$PYTHONPATH
```

To make it public go to cernbox website and share it with `atlas-current-physicists`.
