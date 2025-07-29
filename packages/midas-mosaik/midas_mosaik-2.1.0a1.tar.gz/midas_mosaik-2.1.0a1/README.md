# MIDAS

The MultI-DomAin test Scenario (MIDAS) is a collection of mosaik simulators (https://gitlab.com/mosaik) for smart grid co-simulation and contains a semi-automatic scenario configuration tool.
The latest documentation is always available at https://midas-mosaik.gitlab.io/midas.

Version: 2.0

## Requirements

All required Python packages will be pulled during installation.
However, there are some additional requirements which you have to setup up manually.

First of all, you need a working Python installation >= 3.8. 
Download it from (https://www.python.org/) or use your systems' package manager. 
Furthermore, you will need to have a working Git installation, which you can
find on https://git-scm.com/downloads (or via your package manager).

Midas is able to create an analysis report of the simulation results. 
If you have a working pandoc (https://pandoc.org/) installation, this report will automatically be converted to an .odt file. 
This is **purely optional**.

## Installation

MIDAS is available on https://pypi.org and can be installed, preferably into a virtualenv, with

```bash
pip install midas-mosaik
```

Alternatively, to install directly from the source, you can clone this repository with

```bash
git clone https://gitlab.com/midas-mosaik/midas.git
```

then switch to the midas folder and type

```bash
pip install .
```

for a normal install and 

```bash
pip install -e .
```

for an *editable* install, i.e., changes you make in the source do not require a reinstall.

See the documation at https://midas-mosaik.gitlab.io/midas/installation.html for OS-specific installation instructions. 

## Usage

MIDAS comes with a command line tool called `midasctl` that let's you conveniently start your scenario and/or add minor modifications to it (e.g. change the number of simulations steps, write to a different database, etc.).
`midasctl` also helps doing the initial setup of MIDAS. 
Just type

```bash
midasctl configure
```

and you will be asked to specify where the runtime configuration of MIDAS should be stored and where you want the datasets to be located. You can of course let MIDAS decide this for you, just append `-a` to the command:

```bash
midasctl configure -a
```

Afterwards, you need to download the datasets that MIDAS will use. Type

```bash
midasctl download
```
and wait a moment until MIDAS is done. Finally, you can test your installation with

```bash
midasctl run demo
```

This will run a demonstration scenario and should not take very long.

Pro tip: If you just run the last command, configuration and download will be performed implicitly.


## Data Sets and License

The datasets are pulled from different locations.

The default load profiles are publicly available at https://www.bdew.de/energie/standardlastprofile-strom/

The commercial data set is retrieved from https://data.openei.org/submissions/153 and is released under the Creative Commons License: https://creativecommons.org/licenses/by/4.0/
The energy values are converted from Kilowatt to Megawatt and are slightly rearranged to be usable with MIDAS.

The simbench datasets are directly extracted from the simbench pypi package.

The smart nord dataset comes from the research project Smart Nord (www.smartnord.de).

The Weather datasets are publicly available at https://opendata.dwd.de/ (see the Copyright information: https://www.dwd.de/EN/service/copyright/copyright_node.html)
Since sometimes values are missing, those values are filled with previous orsimilar values.


## MIDAS as Docker

There is a Docker file that can be used to run the MIDAS command line tool.
And there is an install script for those working on LINUX, simply run:

```bash
./build_docker.sh
```

Afterwards, execute

```bash
docker run \
    -v PATH_TO_MIDAS_DATA:/home/user/.config/midas/midas_data \
    -v PATH_TO_OUTPUT_DIR:/app/_outputs \
    midas run midasmv 
```

to run the *midasmv* scenario in the docker. 
Replace `PATH_TO_MIDAS_DATA` with the absolute path to your MIDAS data directory (usually located at ~/.config/midas/midas_data).
Replace `PATH_TO_OUTPUT_DIR` with the location where the outputs should be stored.

If you create a runtime config in the same directory as the Dockerfile before run the build command, this file will be included.
However, you should not change the output_path and the data_path, otherwise you will have to adapt the run command as well.

## Citation

If you want to use Midas in your research, you can cite this publication:

```
@InProceedings{10.1007/978-3-031-43824-0_10,
    author="Balduin, Stephan
    and Veith, Eric M. S. P.
    and Lehnhoff, Sebastian",
    editor="Wagner, Gerd
    and Werner, Frank
    and De Rango, Floriano",
    title="Midas: An Open-Source Framework for Simulation-Based Analysis of Energy Systems",
    booktitle="Simulation and Modeling Methodologies, Technologies and Applications",
    year="2023",
    publisher="Springer International Publishing",
    address="Cham",
    pages="177--194",
    isbn="978-3-031-43824-0"
}


```