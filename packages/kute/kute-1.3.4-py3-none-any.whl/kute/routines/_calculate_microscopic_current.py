# Copyright (c) 2024 The KUTE contributors

from kute.analysis import ElectricCurrent, COMVelocity, PressureTensor
import MDAnalysis
from MDAnalysis.analysis.base import AnalysisBase
import argparse
from ._ascii_logo import print_logo


def get_analysis_class(property:str) -> callable:
    """
    Given a string describing a current, return the corresponding analysis class.

    Args:
        property (str): String describing the current. Currently supported currents are "electric_current", "com_velocity" and "pressure_tensor".

    Raises:
        ValueError: If a current is requested that is not supported

    Returns:
        callable: A class from kute.analysis that calculates the appropriate microscopic current
    """
    equivalence_dictionary ={"electric_current":ElectricCurrent, 
                             "com_velocity": COMVelocity, 
                             "pressure_tensor": PressureTensor}

    if property in equivalence_dictionary:
        return equivalence_dictionary[property]
    
    else:
        raise ValueError("The requested property is not supported. Supported options are " + " ".join(equivalence_dictionary.keys()))


def perform_analysis(universe: MDAnalysis.Universe, 
                     analysis_class: AnalysisBase,
                     filename: str,
                     backend: str = 'serial',
                     n_workers: int = 1) -> None:

    
    analysis = analysis_class(universe, filename)
    if backend == 'serial':
        analysis.run(verbose=True)
    elif backend in ['multiprocessing', 'dask']:
        analysis.run(backend=backend, n_workers=n_workers)
    else:
        raise ValueError("The requested backend is not supported. "
                         "Supported options are 'serial', 'multiprocessing' and 'dask'.")

def main():

    description = "Calculate microscopic currents from MD trajectories. When using this utility, make sure that the selected trajectories contain the appropriate information at the same recording frequencies. The requirements are as follows: Electric current: Topology must include bonds, masses and charges, trajectory must include velocities. Center of mass velocity: Topology must include bonds and masses, trajectory must include velocities. Pressure tensor: Topology must include masses, trajectory must include positions, velocities and forces."

    parser = argparse.ArgumentParser(description=description)

    parser.add_argument("--current", type=str, required=True, metavar="electric_current", help="Type of current to be calculated. Supported options are 'electric_current', 'com_velocity' and 'pressure_tensor'", dest="current")

    parser.add_argument("-f", "--traj", type=str, help="Path to the trajectory file (.trr, .xtc, .dcd, etc.)", metavar="run.trr", required=True, dest="traj")

    parser.add_argument("-t", "--top", type=str, help="Path to the topology file (.gro, .pdb, .tpr, etc.)", metavar="run.tpr", required=True, dest="top")

    parser.add_argument("-o", "--output", type=str, help="Name of the output file", metavar="current.h5", required=False, default="current.h5", dest="output")

    parser.add_argument("-b", "--backend", type=str, help="Backend to be used for the calculation. Supported options are 'serial', 'multiprocessing' and 'dask'. Defaults to 'serial'.", metavar="serial", required=False, default="serial", dest="backend")

    parser.add_argument("-n", "--n_workers", type=int, help="Number of workers to be used in the multiprocessing or dask backend. This value does not make senses with serial backend. Defaults to 1.", metavar="1", required=False, default=1, dest="n_workers")

    args = parser.parse_args()
    print_logo()

    u = MDAnalysis.Universe(args.top, args.traj)
    analysis_class = get_analysis_class(args.current)

    perform_analysis(u, analysis_class, args.output, args.backend, args.n_workers)
    