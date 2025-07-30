# Copyright (c) 2024 The KUTE contributors

import numpy as np
import h5py
from typing import Union, Optional, Tuple
import os
_PATHLIKE = Union[str, bytes, os.PathLike]

def load_electric_current(file: _PATHLIKE, 
                          splits:Optional[int]=1) -> Tuple[np.ndarray, np.ndarray,
                                                              np.ndarray, np.ndarray]:
    """
    Function to load electric currents from h5 files generated with KUTE.

    Args:
        file (str): Path to the h5 file
        splits (int, optional): Number of equal intervals into which the current will be split. Defaults to one.

    Returns:
        t, Jx, Jy, Jz: Time and xyz components of the electric current, given as
                       a proper input to the kute.GreenKuboIntegral class. See
                       that class documentation for more information.
    """

    with h5py.File(file) as f:
        time = np.array(f["timeseries/time"])
        Jx, Jy, Jz = np.array(f["timeseries/current"]).T

    time = np.split(time, splits)[0]
    Jx = np.array(np.split(Jx, splits))
    Jy = np.array(np.split(Jy, splits))
    Jz = np.array(np.split(Jz, splits))

    return time, Jx, Jy, Jz
 

def load_pressure_tensor(file: _PATHLIKE, 
                         splits:Optional[int]=1) -> Tuple[np.ndarray, np.ndarray,
                                                              np.ndarray, np.ndarray]:
    """
    Function to load off-diagonal components of the pressure tensor from h5 files generated with KUTE.

    Args:
        file (str): Path to the h5 file
        splits (int, optional): Number of equal intervals into which the tensor will be split. Defaults to one.

    Returns:
        t, Pxy, Pxz, Pyz: Time and off-diagonal components of the pressure tensor, given as
                          a proper input to the kute.GreenKuboIntegral class. See
                          that class documentation for more information.
    """

    with h5py.File(file) as f:
        time = np.array(f["timeseries/time"])
        Pxy, Pxz, Pyz = np.array(f["timeseries/pressure_tensor"]).T

    time = np.split(time, splits)[0]
    Pxy = np.array(np.split(Pxy, splits))
    Pxz = np.array(np.split(Pxz, splits))
    Pyz = np.array(np.split(Pyz, splits))

    return time, Pxy, Pxz, Pyz

def load_com_velocity(file: _PATHLIKE, resname: str, 
                      splits: Optional[int]=1) -> Tuple[np.ndarray, np.ndarray,
                                                           np.ndarray, np.ndarray]:
    """
    Function to load center of mass velocities for residues from h5 files generated with KUTE.

    Args:
        file (str): Path to the h5 file
        resname (str): Name of the residue for which the center of mass velocity will be loaded.
        splits (int, optional): Number of equal intervals into which the velocity will be split. Defaults to one.

    Returns:
        t, Jx, Jy, Jz: Time and xyz components of the center of mass velocity, given as a proper input to the
                       kute.GreenKuboIntegral class. See that class documentation for more information.

    Raises:
        ValueError: If the requested residue is not present in the file.
    """
    with h5py.File(file) as f:

        if resname not in f["residues"].keys():
            raise ValueError("Residue not present. Available residues are: " + ", ".join(list(f["residues"].keys())))
        
        mask = np.array(f[f"residues/{resname}"])
        time = np.array(f["timeseries/time"])
        Vx, Vy, Vz = np.array(f["timeseries/com_velocities"])[:, mask, :].T

    time = np.split(time, splits)[0]
    Vx = np.vstack(np.split(Vx, splits, axis=1))
    Vy = np.vstack(np.split(Vy, splits, axis=1))
    Vz = np.vstack(np.split(Vz, splits, axis=1))


    return time, Vx, Vy, Vz