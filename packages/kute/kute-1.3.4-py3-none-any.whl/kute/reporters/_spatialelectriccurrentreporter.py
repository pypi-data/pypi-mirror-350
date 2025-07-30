# Copyright (c) 2024 The KUTE contributors

import numpy as np
import h5py

from ._electriccurrentreporter import ElectricCurrentWriter
from kute import __version__
from openmm import unit
from typing import Union
import os
_PATHLIKE = Union[str, bytes, os.PathLike]


class SpatialElectricCurrentReporter(object):
    """
    Custom OpenMM reporter to calculate electric current in a given slice in the z direction

    Args:
        file (str): Name of the file to write the current to
        region (tuple): The values (zmin, zmax) that define the region to calculate the current in. They should be given in Angstroms
    """

    def __init__(self, file: _PATHLIKE, reportInterval: int, region: tuple):

        self._out = h5py.File(file, "w")
        self._writer = None
        self._totalSteps = None

        self._reportInterval = reportInterval

        self._zmin, self._zmax = region

    def __del__(self):
        self._out.close()

    def describeNextReport(self, simulation):
        """
        Function to be called by Openmm, gets information about the next report
        this object will generate.
        """
        steps = self._reportInterval - simulation.currentStep%self._reportInterval

        return (steps, True, True, False, False, True)     
    
    def report(self, simulation, state):
        """
        Function to be called by Openmm, generate a report.
        """
        if self._writer is None:
                self._writer = SpatialElectricCurrentWriter(self._out, simulation, self._zmin, self._zmax)

        positions = state.getPositions(True).value_in_unit(unit.angstrom)
        velocities = state.getVelocities(True).value_in_unit(unit.angstrom/unit.picosecond)
        time = state.getTime().value_in_unit(unit.picosecond)
        self._writer.writeCurrent(time, positions, velocities)


class SpatialElectricCurrentWriter(ElectricCurrentWriter):
     
    def __init__(self, file: h5py.File, simulation, zmin: float, zmax: float):
        """Class to write electric current in binary h5 format. Helper to SpatialElectricCurrentReporter

        Args:
            file (h5py.File): File where information will be written
            simulation : OpenMM object describing the simulation
            zmin (float): Minimum z value of the region to calculate the current in
            zmax (float): Maximum z value of the region to calculate the current in
        """

        self._zmin = zmin
        self._zmax = zmax
        super().__init__(file, simulation)
 
    def writeCurrent(self, time: np.ndarray, positions: np.ndarray, velocities: np.ndarray):
        """
        Function to calculate the electric current and write it to the file
        """
        z = positions[:, 2]
        mask = (z > self._zmin) & (z < self._zmax)
        current = np.sum(velocities[mask, :]*self._weight_vector[mask, np.newaxis], axis=0)

        LEN = self._file['timeseries/time'].shape[0]
        self._file['timeseries/time'].resize((LEN+1,))
        self._file['timeseries/time'][-1] = time
        self._file['timeseries/current'].resize((LEN+1,3))
        self._file['timeseries/current'][-1] = current
   