# Copyright (c) 2024 The KUTE contributors

import getpass
import os

import h5py
import MDAnalysis as mda
from MDAnalysis.analysis.base import Results
import numpy as np
import pytest

from kute import __version__
from kute.analysis import ElectricCurrent, COMVelocity, PressureTensor

try:
    import dask
    SKIP_DASK = False
except:
    SKIP_DASK = True

ACTUAL_PATH = os.path.split(os.path.join(os.path.abspath(__file__)))[0]

@pytest.fixture
def universe():
    topo = os.path.join(ACTUAL_PATH, "files_for_tests/inputs/topo.tpr")
    traj = os.path.join(ACTUAL_PATH, "files_for_tests/inputs/traj.trr")
    return mda.Universe(topo, traj)

@pytest.fixture
def traj_length():
    topo = os.path.join(ACTUAL_PATH, "files_for_tests/inputs/topo.tpr")
    traj = os.path.join(ACTUAL_PATH, "files_for_tests/inputs/traj.trr")

    return len(mda.Universe(topo, traj).trajectory)

@pytest.fixture
def n_atoms():
    topo = os.path.join(ACTUAL_PATH, "files_for_tests/inputs/topo.tpr")
    traj = os.path.join(ACTUAL_PATH, "files_for_tests/inputs/traj.trr")

    return len(mda.Universe(topo, traj).atoms)

@pytest.fixture
def n_residues():
    topo = os.path.join(ACTUAL_PATH, "files_for_tests/inputs/topo.tpr")
    traj = os.path.join(ACTUAL_PATH, "files_for_tests/inputs/traj.trr")

    return len(mda.Universe(topo, traj).residues)

@pytest.fixture
def resnames():
    topo = os.path.join(ACTUAL_PATH, "files_for_tests/inputs/topo.tpr")
    traj = os.path.join(ACTUAL_PATH, "files_for_tests/inputs/traj.trr")

    return np.unique(mda.Universe(topo, traj).residues.resnames)

@pytest.fixture
def results_current():

    file = os.path.join(ACTUAL_PATH, "files_for_tests/results/results_current_test.h5")
    return h5py.File(file)

@pytest.fixture
def results_com_velocity():
    file = os.path.join(ACTUAL_PATH, "files_for_tests/results/results_com_velocity_test.h5")
    return h5py.File(file, "r")

@pytest.fixture
def results_pressure_tensor():
    file = os.path.join(ACTUAL_PATH, "files_for_tests/results/results_pressure_tensor_test.h5")
    return h5py.File(file, "r")

@pytest.fixture
def run_class(class_name, universe, backend):
    current = class_name(universe, filename=os.path.join(ACTUAL_PATH, "temp_file.h5"))
    if backend == "serial":
        current.run(backend=backend)
    else:
        current.run(backend=backend, n_workers=2)
    return current

class TestElectricCurrent(object):

    def test_init(self, universe):
        
        current = ElectricCurrent(universe)

        assert current.u == universe
        assert current._trajectory == universe.trajectory
        assert current.filename == "current.h5"
        assert current.results == Results()

        current = ElectricCurrent(universe, "test.h5")

        assert current.u == universe
        assert current._trajectory == universe.trajectory
        assert current.filename == "test.h5"
        assert current.results == Results()

    @pytest.mark.parametrize('class_name', [ElectricCurrent])
    @pytest.mark.parametrize('backend', [
                                        'serial', 
                                         'multiprocessing', 
                                         pytest.param('dask', marks=pytest.mark.skipif(SKIP_DASK, reason="Dask is not installed"))
                                         ])
    def test_analyze(self, universe, run_class, results_current, traj_length, n_atoms):

        ## Initialize analysis 

        current = run_class

        ## Check if internal variables make sense

        assert len(current._weights) == n_atoms
        assert current.results.current.shape == (traj_length, 3)

        ## Check if the file was correctly saved

        assert os.path.isfile(os.path.join(ACTUAL_PATH, "temp_file.h5"))

        ## Check for metadata information

        with h5py.File(os.path.join(ACTUAL_PATH, "temp_file.h5"), "r") as f:

            assert f["information"].attrs["kute_version"] == __version__
            assert f["information"].attrs["author"] == getpass.getuser()
            assert f["information/units"].attrs["time"] == "ps"
            assert f["information/units"].attrs["electric_current"] == "e * A / ps"
            
            assert np.allclose(np.array(f["timeseries/time"]), np.array(results_current["timeseries/time"]))
            assert np.allclose(np.array(f["timeseries/current"]), np.array(results_current["timeseries/current"]))
            calculated_current_step_1 =  np.array(f["timeseries/current"])[0]

       ## Calculate for first frame manually

        masses = universe.atoms.masses
        residue_masses = np.array([ a.residue.mass for a in universe.atoms ])
        residue_charges = np.array([ a.residue.charge for a in universe.atoms ])
        weights = masses * residue_charges / residue_masses
        velocities = universe.atoms.velocities

        true_current_step_1 = np.sum(weights[:, np.newaxis] * velocities, axis=0)

        assert np.allclose(true_current_step_1, calculated_current_step_1)

        os.remove(os.path.join(ACTUAL_PATH, "temp_file.h5"))

class TestPressureTensor(object):

    def test_init(self, universe):
        
        pressure = PressureTensor(universe)

        assert pressure.u == universe
        assert pressure._trajectory == universe.trajectory
        assert pressure.filename == "pressure_tensor.h5"
        assert pressure.results == Results()

        pressure = PressureTensor(universe, "test.h5")

        assert pressure.u == universe
        assert pressure._trajectory == universe.trajectory
        assert pressure.filename == "test.h5"
        assert pressure.results == Results()
    
    @pytest.mark.parametrize('class_name', [PressureTensor])
    @pytest.mark.parametrize('backend', [
                                    'serial', 
                                        'multiprocessing', 
                                        pytest.param('dask', marks=pytest.mark.skipif(SKIP_DASK, reason="Dask is not installed"))
                                        ])
    def test_analyze(self, universe, run_class, results_pressure_tensor, traj_length):

        ## Initialize analysis 

        pressure = run_class

        ## Check if internal variables make sense

        assert pressure.results.off_diagonal.shape == (traj_length, 3)

        ## Check if the file was correctly saved

        assert os.path.isfile(os.path.join(ACTUAL_PATH, "temp_file.h5"))

        ## Check for metadata information

        with h5py.File(os.path.join(ACTUAL_PATH, "temp_file.h5"), "r") as f:

            assert f["information"].attrs["kute_version"] == __version__
            assert f["information"].attrs["author"] == getpass.getuser()
            assert f["information/units"].attrs["time"] == "ps"
            assert f["information/units"].attrs["pressure_tensor"] == "Pa"
            
            assert np.allclose(np.array(f["timeseries/time"]), np.array(results_pressure_tensor["timeseries/time"]))
            assert np.allclose(np.array(f["timeseries/pressure_tensor"]), np.array(results_pressure_tensor["timeseries/pressure_tensor"]), rtol=1e-2)
            calculated_pressure_step_1 =  np.array(f["timeseries/pressure_tensor"])[0]

       ## Calculate for first frame manually

        masses = universe.atoms.masses * 1.66054e-27
        positions = universe.atoms.positions * 1e-10
        velocities = universe.atoms.velocities * 1e-10 / 1e-12
        forces = universe.atoms.forces * 1e3 / (1e-10 * 6.02214076e23)
        volume = universe.dimensions[:3].prod() * 1e-30

        pxy = np.sum(masses * velocities[:, 0] * velocities[:, 1]) / volume + np.sum(positions[:, 0] * forces[:, 1]) / volume
        pxz = np.sum(masses * velocities[:, 0] * velocities[:, 2]) / volume + np.sum(positions[:, 0] * forces[:, 2]) / volume
        pyz = np.sum(masses * velocities[:, 1] * velocities[:, 2]) / volume + np.sum(positions[:, 1] * forces[:, 2]) / volume

        off_diagonal = np.array([pxy, pxz, pyz])

        assert np.allclose(off_diagonal, calculated_pressure_step_1)


class TestCOMVelocity(object):

    def test_init(self, universe):
        
        vel = COMVelocity(universe)

        assert vel.u == universe
        assert vel._trajectory == universe.trajectory
        assert vel.filename == "com_velocity.h5"
        assert vel.results == Results()

        vel = COMVelocity(universe, "test.h5")

        assert vel.u == universe
        assert vel._trajectory == universe.trajectory
        assert vel.filename == "test.h5"
        assert vel.results == Results()

    @pytest.mark.parametrize('class_name', [COMVelocity])
    @pytest.mark.parametrize('backend', [
                                        'serial', 
                                        'multiprocessing', 
                                        pytest.param('dask', marks=pytest.mark.skipif(SKIP_DASK, reason="Dask is not installed"))
                                        ])
    def test_analyze(self, universe, run_class, results_com_velocity, traj_length, n_atoms, n_residues, resnames):

        vel = run_class
        
        ## Check if internal variables make sense https://docs.mdanalysis.org/stable/documentation_pages/coordinates_modules.html

        assert vel._matrix.shape == (n_residues, n_atoms)
        assert vel.results.com_vel.shape == (traj_length, n_residues, 3)

        ## Check for metadata information

        with h5py.File(os.path.join(ACTUAL_PATH, "temp_file.h5"), "r") as f:

            # General information

            assert f["information"].attrs["kute_version"] == __version__
            assert f["information"].attrs["author"] == getpass.getuser()
            assert f["information/units"].attrs["time"] == "ps"
            assert f["information/units"].attrs["com_velocities"] == "A / ps"

            # Residue identificators

            for res in resnames:

                assert res in f["residues"].keys()
                assert np.all(np.array(f[f"residues/{res}"]) == np.array(results_com_velocity[f"residues/{res}"]))
                assert len(np.array(f[f"residues/{res}"])) == len(universe.select_atoms(f"resname {res}").residues)

            # Check result

            assert np.allclose(np.array(f["timeseries/time"]), np.array(results_com_velocity["timeseries/time"]))
            assert np.allclose(np.array(f["timeseries/com_velocities"]), np.array(results_com_velocity["timeseries/com_velocities"]))

        ## Manually calculate the result for the first frame, and the for the first residue of each kind

        for resname in resnames:

            residue = universe.residues[np.where(universe.residues.resnames == resname)[0][0]]
            true_velocity = np.zeros(3)

            for atom in residue.atoms:

                true_velocity += atom.mass / residue.mass * atom.velocity
            
            with h5py.File(os.path.join(ACTUAL_PATH, "temp_file.h5"), "r") as f:
                
                index = np.array(f[f"residues/{resname}"])[0]
                calculated_velocity = np.array(f[f"timeseries/com_velocities"])[0, index, :]

            assert np.allclose(true_velocity, calculated_velocity)
            

        os.remove(os.path.join(ACTUAL_PATH, "temp_file.h5"))
