# Copyright (c) 2024 The KUTE contributors

import argparse
import numpy as np
import MDAnalysis as mda

from typing import Tuple
from ._ascii_logo import print_logo
from kute import GreenKuboIntegral, IntegralEnsemble
from kute.loaders import load_electric_current, load_com_velocity, load_pressure_tensor



def get_loader_function(string:str, resname:str=None) -> callable:
    """Given an input string describing a transport coefficient, return the corresponding loader function.

    Args:
        string (str): String describing the transport coefficient
        resname (str, optional): Name of the residue for which to calculate the diffusion coefficient. Defaults to None.

    Raises:
        ValueError: If a transport coefficient is requested that is not supported

    Returns:
        callable: A function from kute.loaders that loads the appropriate microscopic current
    """

    if string == "diffusion_coefficient" and resname is None:
        raise ValueError("The residue name is required to calculate the diffusion coefficient")

    equivalence_dictionary = {"electric_conductivity": load_electric_current, 
                              "diffusion_coefficient": lambda filename, splits: load_com_velocity(file=filename, resname=resname, splits=splits), 
                              "viscosity": load_pressure_tensor}

    if string in equivalence_dictionary:
        return equivalence_dictionary[string]
    
    else:
        raise ValueError("The requested transport coefficient is not supported. Supported options are " + " ".join(equivalence_dictionary.keys()))
    

def calculation_for_one(filename:str, loader:callable, splits:int, weight_file:str=None) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Runs the calculation for a single current file

    Args:
        filename (str): Name of the .h5 file containing the microscopic current
        loader (callable): A function from kute.loaders that loads the appropriate microscopic current
        splits (int): Number of splits to use for the Green-Kubo integral
        weight_file (str, optional): Name of the file containing extra multiplicative factors. Defaults to None.

    Returns:
        Tuple[np.ndarray, np.ndarray, np.ndarray]: lag time, isotropic average running transport coefficient, uncertainty
    """

    if weight_file is not None:
        weight = np.loadtxt(weight_file)
    else:
        weight = 1

    t, Jx, Jy, Jz = loader(filename, splits)
    integral = GreenKuboIntegral(t, Jx, Jy, Jz)
    tavg, avg, u_avg = integral.get_isotropic_running_average()

    avg *= weight
    u_avg *= weight

    return tavg, avg, u_avg


def calculation_for_ensemble(filenames:iter, loader:callable, splits:int, weight_file:str=None)-> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Runs the calculation for any number of .h5 files, treating them as an ensemble

    Args:
        filename (iter): An iterable containing the names of the .h5 files containing the microscopic current
        loader (callable): A function from kute.loaders that loads the appropriate microscopic current
        splits (int): Number of splits to use for the Green-Kubo integral
        weight_file (str, optional): Name of the file containing extra multiplicative factors. Defaults to None.

    Returns:
        Tuple[np.ndarray, np.ndarray, np.ndarray]: lag time, isotropic average transport coefficient, uncertainty
    """

    if weight_file is not None:
        weights = np.loadtxt(weight_file)
    else:
        weights = weight_file

    integrals = []
    for name in filenames:
        t, Jx, Jy, Jz = loader(name, splits)
        integrals.append(GreenKuboIntegral(t, Jx, Jy, Jz))
    
    ensemble = IntegralEnsemble(integrals, factors=weights)
    return ensemble.get_isotropic_average()


def save_results(out_file:str, tavg:np.ndarray, avg:np.ndarray, uavg:np.ndarray):
    """Save the results of the calculation to a file

    Args:
        out_file (str): Name of the file to save the results to
        tavg (np.ndarray): Lag time
        avg (np.ndarray): Isotropic average transport coefficient
        uavg (np.ndarray): Uncertainty
    """

    to_save = np.vstack([tavg, avg, uavg]).T
    np.savetxt(out_file, to_save, header="Time       Average         Uncertainty")


def main():

    description = "Calculates the isotropic transport coefficient as a function of averaging cutoff"

    parser = argparse.ArgumentParser(description=description)

    ## Input arguments

    parser.add_argument("-f", required=True, type=str, dest="h5_files", metavar="current.h5", nargs="+", help = "List of h5 binary files containing the microscopic current for each replica.")

    parser.add_argument("--splits", required=False, type=int, dest="splits", metavar="1", default=1, help = "Number of fragments of equal size into which to split the pressure tensor of each replica")

    parser.add_argument("--weights", required=False, type=str, dest="weights", metavar="weights.txt", default=None, help = "File containing the weighting factor for each replica. Can be used to change units or to include replica-dependent values such as the volume")

    parser.add_argument("--property", required=True, type=str, dest="property", metavar="electric_conductivity", help = "The transport coefficient to calculate. Supported options are electric_conductivity, diffusion_coefficient and viscosity")

    parser.add_argument("--resname", required=False, type=str, dest="resname", metavar="resname", default=None, help = "Name of the residue for which to calculate the diffusion coefficient. Not required for the other transport coefficients")

    ## Output arguments

    parser.add_argument("-o", "--output", required=False, type=str, dest="output", metavar="output.dat", default="transport_coefficient.dat", help="Name of the file to save the results to")

    ## Load the arguments, print the KUTE logo

    args = parser.parse_args()
    print_logo()

    ## Get the loader function. In the case of diffusion coefficient, modify it to include the resname argument

    loader = get_loader_function(args.property, args.resname)

    ## Run the calculation

    if len(args.h5_files) == 1:
        tavg, avg, uavg = calculation_for_one(args.h5_files[0], loader, args.splits, args.weights)

    else:
        tavg, avg, uavg = calculation_for_ensemble(args.h5_files, loader, args.splits, args.weights)

    ## Save the results

    save_results(args.output, tavg, avg, uavg)

if __name__ == "__main__":
    main()

            
