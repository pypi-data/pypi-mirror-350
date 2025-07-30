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

class COMVelocityReporter(object):
    """
    Custom OpenMM reporter to save center of mass velocities

    Args:
        file (str): Name of the file to write the velocities to

    """

    def __init__(self, file: _PATHLIKE, reportInterval: int):
        self._out = h5py.File(file, "w")
        self._reportInterval = reportInterval
        self._writer = None
    
    def __del__(self):
        self._out.close()
    
    def describeNextReport(self, simulation):
        """
        Function to be called by Openmm, gets information about the next report
        this object will generate.
        """

        steps = self._reportInterval - simulation.currentStep%self._reportInterval

        return (steps, False, True, False, False, None)

    def report(self, simulation, state):
        """
        Function to be called by Openmm, generate a report.
        """
        if self._writer is None:

            self._writer = COMVelocityWriter(self._out, simulation)


        velocities = state.getVelocities(True).value_in_unit(unit.angstrom/unit.picosecond)
        time = state.getTime().value_in_unit(unit.picosecond)
        self._writer.writeVelocities(time, velocities)


class COMVelocityWriter(object):
    """Class to write center of mass velocities. Helper to COMVelocityReporter
    Args:
        file (h5py.File): File where information will be written
        simulation : OpenMM object describing the simulation
    """

    def __init__(self, file: h5py.File, simulation):
        self._file = file
        self._calculateWeights(simulation)
        self._prepareWriter(simulation)


    def _calculateWeights(self, simulation):


        system = simulation.context.getSystem()

        self._atom_residuemass = np.array([0.0 for _ in simulation.topology.atoms()])
        self._atom_masses = np.array([0.0 for _ in simulation.topology.atoms()])

        ## Set the mass of the residue to which each atom belongs

        for residue in simulation.topology.residues():

            mass = 0
            for atom in residue.atoms():
                mi = system.getParticleMass(atom.index).value_in_unit(unit.dalton)
                mass += mi
                self._atom_masses[atom.index] = mi

            for atom in residue.atoms():
                self._atom_residuemass[atom.index] = mass

        ## Eliminate the divergency. We will put the weight to one, so that we calculate the velocity and not the com_velocicy
        ## These can correspond, for example, to electrostatic images in constant potential simulations

        where_zero_mass = self._atom_residuemass==0
        self._atom_masses[where_zero_mass] = 0
        self._atom_residuemass[where_zero_mass] = 1

        ## Carry on the calculation
        ## Determine a N_residues x N_atoms matrix such that M @ V_atoms = V_residues


        self._weight_vector = self._atom_masses / self._atom_residuemass
        self._n_atoms = len(self._weight_vector)
        self._n_residues = np.array([1 for _ in simulation.topology.residues()]).sum()
        self._matrix = np.zeros((self._n_residues, self._n_atoms))

        for i, res in enumerate(simulation.topology.residues()):
            for atom in res.atoms():
                j = atom.index
                self._matrix[i, j] = self._weight_vector[j]

        ## Reduce the size of the matrix
        ## If a given column is only zeroes, it means that the corresponding atom is not involved in the calculation (massless, or belongs to a massles residue)

        self.massless_residues = np.all(self._matrix==0, axis=1)
        self.N_MASSIVE_RESIDUES = np.sum(~self.massless_residues)
        self.MATRIX = self._matrix[~self.massless_residues, :]

        ## Now, the operation self.MATRIX @ V_atoms yields a vector with the COM velocity of massive residues.
        ## However, many of the atoms are not used, and the matrix will be needlesly big
        ## We can also prune the columns of the matrix to eliminate the atoms that belong to massless residues

        self.ATOM_MASK = np.ones(self._n_atoms, dtype=bool)

        for i, r in enumerate(simulation.topology.residues()):
            if self.massless_residues[i]:
                for a in r.atoms():
                    self.ATOM_MASK[a.index] = False

        self.MATRIX = self.MATRIX[:, self.ATOM_MASK]

        print("POR FAVOR QUE FUNCIONE")

    def _prepareWriter(self, simulation):

        # Create metadata group

        self._file.create_group('information')
        self._file['information'].attrs['kute_version'] = __version__
        self._file['information'].attrs['openmm_version'] = openmm.Platform.getOpenMMVersion()
        self._file['information'].attrs['author'] = getpass.getuser()
        self._file['information'].create_group('units')
        self._file['information/units'].attrs['time'] = "ps"
        self._file['information/units'].attrs['com_velocities'] = "A / ps"

        ## Create identificators for which parts corresponds to which residue

        self._file.create_group("residues")
        names = []
        for i, r in enumerate(simulation.topology.residues()):
            
            ## We have to check that this is not a massless residue
            is_massive = ~self.massless_residues[i]
            if is_massive:
                names.append(r.name)

        names = np.array(names)
        for name in np.unique(names):
            where = np.where(names==name)[0]
            self._file['residues'].create_dataset(name, data=where, dtype=int)


        # Create velocity group

        self._file.create_group('timeseries')

        self._file['timeseries'].create_dataset('time', shape=(0, ), maxshape=(None,), dtype=float)
        self._file['timeseries'].create_dataset(f'com_velocities', shape=(0, self.N_MASSIVE_RESIDUES,3), maxshape=(None, self.N_MASSIVE_RESIDUES, 3), dtype=float)
        

    def writeVelocities(self, time: float, velocities: np.ndarray):
        """Write the center of mass velocities to the file

        Args:
            time (float): current value of the simulation time
            velocities (np.ndarray): Velocities of all the atoms in the system
        """
        com_velocities = self.MATRIX @ velocities[self.ATOM_MASK]
        LEN = self._file['timeseries/time'].shape[0]
        self._file['timeseries/time'].resize((LEN+1,))
        self._file['timeseries/time'][-1] = time
        self._file[f'timeseries/com_velocities'].resize((LEN+1, self.N_MASSIVE_RESIDUES, 3))
        self._file[f'timeseries/com_velocities'][-1] = com_velocities