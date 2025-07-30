# Copyright (c) 2024 The KUTE contributors

import numpy as np
import getpass
import h5py
import openmm

from kute import __version__
from openmm import unit
from typing import Union
import os
_PATHLIKE = Union[str, bytes, os.PathLike]

class PressureTensorReporter(object):
    """
    Custom OpenMM reporter to save the off-diagonal components of the pressure tensor.

    Args:
        file (str): Name of the file to write the pressure tensor to
    """

    def __init__(self, file: _PATHLIKE, reportInterval: int):


        self._out = h5py.File(file, "w")
        self._writer = None
        self._totalSteps = None

        self._reportInterval = reportInterval

    def __del__(self):
        self._out.close()

    def describeNextReport(self, simulation):
        """
        Function to be called by Openmm, gets information about the next report
        this object will generate.
        """
        steps = self._reportInterval - simulation.currentStep%self._reportInterval

        return (steps, True, True, True, False, False)
    

    def report(self, simulation, state):

        if self._writer is None:
            self._writer = PressureTensorWriter(self._out, simulation)

        volume = state.getPeriodicBoxVolume().value_in_unit(unit.meter**3)
        positions = state.getPositions(True).value_in_unit(unit.angstrom)
        velocities = state.getVelocities(True).value_in_unit(unit.angstrom/unit.picosecond)
        forces = state.getForces(True).value_in_unit(unit.kilojoule_per_mole/unit.angstrom)
        time = state.getTime().value_in_unit(unit.picosecond)

        self._writer.writePressureTensor(time, positions, velocities, forces, volume) 


class PressureTensorWriter(object):

    def __init__(self, file: h5py.File, simulation):
        """Class to write electric current in binary h5 format. Helper to PressureTensorReporter

        Args:
            file (h5py.File): File where information will be written
            simulation : OpenMM object describing the simulation
        """
        self._file = file
        self._calculateWeights(simulation)
        self._prepareWriter()

    def _calculateWeights(self, simulation):

        system = simulation.context.getSystem()
        D_TO_KG = 1.66054e-27
        NA = 6.02214076e23
        self._UNITS_FIRST_TERM = D_TO_KG * (1e-10)**2 / ((1e-12)**2) # Units will be J
        self._UNITS_SECOND_TERM = 1_000 / NA # Units will be J

        self._atom_masses = np.array([0.0 for _ in simulation.topology.atoms()])

        ## Set the mass of the residue to which each atom belongs
        for residue in simulation.topology.residues():
            mass = 0
            for atom in residue.atoms():
                mi = system.getParticleMass(atom.index).value_in_unit(unit.dalton)
                mass += mi
                self._atom_masses[atom.index] = mi



    def _prepareWriter(self):

        # Create metadata group

        self._file.create_group('information')
        self._file['information'].attrs['kute_version'] = __version__
        self._file['information'].attrs['openmm_version'] = openmm.Platform.getOpenMMVersion()
        self._file['information'].attrs['author'] = getpass.getuser()
        self._file['information'].create_group('units')
        self._file['information/units'].attrs['time'] = "ps"
        self._file['information/units'].attrs['pressure_tensor'] = "Pa" 

        # create a group for the pressure tensor

        self._file.create_group('timeseries')

        self._file['timeseries'].create_dataset('time', shape=(0, ), maxshape=(None,), dtype=float)
        self._file['timeseries'].create_dataset(f'pressure_tensor', shape=(0, 3), maxshape=(None, 3), dtype=float)

    def writePressureTensor(self, time: float, positions: np.ndarray, velocities: np.ndarray, forces: np.ndarray, volume: float):
        """Write the (center of mass) off-diagonal components of the pressure tensor to the file

        Args:
            time (float): current value of the simulation time
            positions (np.ndarray): Positions of all the atoms in the system
            velocities (np.ndarray): Velocities of all the atoms in the system
            forces (np.ndarray): Forces of all the atoms in the system
        """
        

        pressure_tensor = np.triu(self._UNITS_FIRST_TERM * np.tensordot(self._atom_masses[:, np.newaxis]*velocities, velocities, axes=(0, 0)) + self._UNITS_SECOND_TERM * np.tensordot(positions, forces, axes=(0, 0)), k=1)
        
        off_diagonal = pressure_tensor.flatten()[np.flatnonzero(pressure_tensor)] / volume

        ## Save the results

        LEN = self._file['timeseries/time'].shape[0]
        self._file['timeseries/time'].resize((LEN+1,))
        self._file['timeseries/time'][-1] = time
        self._file[f'timeseries/pressure_tensor'].resize((LEN+1, 3))
        self._file[f'timeseries/pressure_tensor'][-1] = off_diagonal