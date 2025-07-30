![logo](kute.png){width=50%}
# KUTE: green-Kubo Uncertainty-based Transport properties Estimator
[![pipeline status](https://gitlab.com/nafomat/kute/badges/main/pipeline.svg)](https://gitlab.com/nafomat/kute/-/commits/main)
[![coverage report](https://gitlab.com/nafomat/kute/badges/main/coverage.svg)](https://gitlab.com/nafomat/kute/-/commits/main)
[![Latest Release](https://gitlab.com/nafomat/kute/-/badges/release.svg)](https://gitlab.com/nafomat/kute/-/releases)

Kute is a python module designed for the calculation of Green-Kubo integrals from molecular dynamics simulations. It includes features to calculate said integrals when the microscopic currents are known, as well as tools to compute these. Its workflow is summarized in the figure below
![kute_flowchart](https://gitlab.com/nafomat/kute/-/raw/main/doc/source/kute_flowchart.png)

## Installation
To install KUTE, just clone this repository and run the following command 

```
python -m pip install -e .
```

or use pip

```
pip install kute
```

with that, KUTE will be available both as a python module and as commandline functions that can be invoked.

## Installing the LAMMPS plugin

Installation of the LAMMPS plugin requires the (re)compilation of LAMMPS. The contents of the lammps folder of this repository should be copied into the src folder of LAMMPS before the compilation. After that the _current_ compute should be available (for more information check the [documentation](https://nafomat.gitlab.io/kute/get_currents.html#using-lammps)).

## Documentation and quick start guide

The documentation, as well a a quick tutorial can be seen [here](https://nafomat.gitlab.io/kute)

## Cite us

If you found this useful, please consider citing our paper:

	- https://doi.org/10.1021/acs.jcim.4c02219
