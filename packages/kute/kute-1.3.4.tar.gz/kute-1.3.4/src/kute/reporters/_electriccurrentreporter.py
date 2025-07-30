# Copyright (c) 2024 The KUTE contributors

import numpy as np
import getpass
import openmm
import h5py

from kute import __version__
from openmm import unit
from typing import Union
import os
_PATHLIKE = Union[str, bytes, os.PathLike]

class ElectricCurrentReporter(object):
    """
    Custom OpenMM reporter to save electric current

    Args:
        file (str): Name of the file to write the current to

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

        return (steps, False, True, False, False, None)

    def report(self, simulation, state):
        """
        Function to be called by Openmm, generate a report.
        """
        if self._writer is None:
                self._writer = ElectricCurrentWriter(self._out, simulation)


        velocities = state.getVelocities(True).value_in_unit(unit.angstrom/unit.picosecond)
        time = state.getTime().value_in_unit(unit.picosecond)
        self._writer.writeCurrent(time, velocities)


class ElectricCurrentWriter(object):

    def __init__(self, file: h5py.File, simulation):
        """Class to write electric current in binary h5 format. Helper to ElectricCurrentReporter

        Args:
            file (h5py.File): File where information will be written
            simulation : OpenMM object describing the simulation
        """
        self._file = file
        self._calculateWeights(simulation)
        self._prepareWriter()

    def _calculateWeights(self, simulation):

        ## Electric current can be calculated as a sum over all atoms
        ## j = q_i m_i v_i / M_i = (Q_i * m_i / M_i) * v_i = w_i * v_i
        ## Uppercase: residue property. Lowercase: atomic property
        ## we want to compute the weight vector w_i.

        system = simulation.context.getSystem()
        atom_charges = []
        nonbonded = [f for f in system.getForces() if isinstance(f, openmm.NonbondedForce)][0]

        for i in range(system.getNumParticles()):
            charge, _, _ = nonbonded.getParticleParameters(i)
            atom_charges.append(charge)

        atom_charges = np.array(atom_charges)

        self._atom_residuemass = np.array([0.0 for _ in simulation.topology.atoms()])
        self._atom_residuecharge = np.array([0.0 for _ in simulation.topology.atoms()])
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

        ## Set the charge of the residue to which each atom belongs

        for residue in simulation.topology.residues():

            q = 0
            for atom in residue.atoms():
                q += atom_charges[atom.index].value_in_unit(unit.elementary_charge)

            for atom in residue.atoms():
                self._atom_residuecharge[atom.index] = q

        self._weight_vector = self._atom_residuecharge * self._atom_masses / self._atom_residuemass


    def _prepareWriter(self):

        # Create metadata group
    
        self._file.create_group('information')
        self._file['information'].attrs['kute_version'] = __version__
        self._file['information'].attrs['openmm_version'] = openmm.Platform.getOpenMMVersion()
        self._file['information'].attrs['author'] = getpass.getuser()
        self._file['information'].create_group('units')
        self._file['information/units'].attrs['time'] = "ps"
        self._file['information/units'].attrs['electric_current'] = "e * A / ps"

        # Create current group

        self._file.create_group('timeseries')
        self._file['timeseries'].create_dataset('time', shape=(0, ), maxshape=(None,), dtype=float)
        self._file['timeseries'].create_dataset('current', shape=(0, 3), maxshape=(None, 3), dtype=float)


    def writeCurrent(self, time: np.ndarray, velocities:np.ndarray):

        current = np.sum(velocities*self._weight_vector[:, np.newaxis], axis=0)

        LEN = self._file['timeseries/time'].shape[0]
        self._file['timeseries/time'].resize((LEN+1,))
        self._file['timeseries/time'][-1] = time
        self._file['timeseries/current'].resize((LEN+1,3))
        self._file['timeseries/current'][-1] = current
