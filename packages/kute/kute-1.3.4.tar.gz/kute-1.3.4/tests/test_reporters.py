# Copyright (c) 2024 The KUTE contributors

import os 
import pytest
import getpass 
import h5py
import numpy as np

from kute import __version__
from kute.loaders import load_electric_current, load_com_velocity, load_pressure_tensor

try: 
    import openmm
    from openmm import unit
    import openmm.app as app

    from kute.reporters import ElectricCurrentReporter, COMVelocityReporter, PressureTensorReporter, SpatialElectricCurrentReporter

    SKIP_TESTS = False

except ImportError:
    SKIP_TESTS = True


ACTUAL_PATH = os.path.split(os.path.join(os.path.abspath(__file__)))[0]
TOTALSTEPS = 100

@pytest.fixture
def simulation():

    FIELD = os.path.join(ACTUAL_PATH, "files_for_tests/inputs/field_openmm.xml")
    CONFIG = os.path.join(ACTUAL_PATH, "files_for_tests/inputs/config_openmm.pdb")
    
    TEMP = 300 * unit.kelvin
    TIMESTEP = 1.0 * unit.femtosecond

    forcefield = app.ForceField(FIELD)
    pdb = app.PDBFile(CONFIG)

    system = forcefield.createSystem(pdb.topology,
                                     nonbondedMethod=app.PME,
                                     nonbondedCutoff=12.0*unit.angstrom,
                                     constraints=app.HBonds,
                                     ewaldErrorTolerance=1.0e-5)

    integrator = openmm.NoseHooverIntegrator(TEMP, 10 / unit.picoseconds, TIMESTEP)
    sim = app.Simulation(pdb.topology, system, integrator)
    sim.context.setPositions(pdb.positions)
    sim.context.setVelocitiesToTemperature(TEMP)

    return sim


class TestElectricCurrentReporter(object):

    @pytest.mark.skipif(SKIP_TESTS, reason="OpenMM is not installed")
    def test_reporter(self, simulation):

        simulation.reporters.clear()
        
        current_reporter = ElectricCurrentReporter(os.path.join(ACTUAL_PATH, "report_current_temp.h5"), reportInterval=1)
        simulation.reporters.append(current_reporter)

        simulation.step(TOTALSTEPS)

        # To close the reporter object
        simulation.reporters.clear()
        del current_reporter

        # Check if report exists

        FILEPATH = os.path.join(ACTUAL_PATH, "report_current_temp.h5")
        assert os.path.isfile(FILEPATH)

        ## Check if the file can be loaded with KUTE

        t, Jx, Jy, Jz = load_electric_current(FILEPATH)
        
        assert Jx.shape == (1, len(t))
        assert Jy.shape == (1, len(t))
        assert Jz.shape == (1, len(t))

        # Checks for the h5 file

        with h5py.File(FILEPATH, "r") as f:

            # Check general information

            assert f["information"].attrs["kute_version"] == __version__
            assert f["information"].attrs["author"] == getpass.getuser()
            assert f["information/units"].attrs["time"] == "ps"
            assert f["information/units"].attrs["electric_current"] == "e * A / ps"

            # Check for correct shapes

            assert len(np.array(f["timeseries/time"])) == TOTALSTEPS
            assert np.array(f["timeseries/current"]).shape == (TOTALSTEPS, 3)

        os.remove(FILEPATH)

class TestSpatialElectricCurrentReporter(object):

    @pytest.mark.skipif(SKIP_TESTS, reason="OpenMM is not installed")
    @pytest.mark.parametrize("region", [(1, 2), (3, 4), (5, 6)])
    def test_reporter(self, simulation, region):

        simulation.reporters.clear()
        
        current_reporter = SpatialElectricCurrentReporter(os.path.join(ACTUAL_PATH, "report_current_temp.h5"), reportInterval=1, region=region)
        simulation.reporters.append(current_reporter)

        simulation.step(TOTALSTEPS)

        # To close the reporter object
        simulation.reporters.clear()
        del current_reporter

        # Check if report exists

        FILEPATH = os.path.join(ACTUAL_PATH, "report_current_temp.h5")
        assert os.path.isfile(FILEPATH)

        ## Check if the file can be loaded with KUTE

        t, Jx, Jy, Jz = load_electric_current(FILEPATH)
        
        assert Jx.shape == (1, len(t))
        assert Jy.shape == (1, len(t))
        assert Jz.shape == (1, len(t))

        # Checks for the h5 file

        with h5py.File(FILEPATH, "r") as f:

            # Check general information

            assert f["information"].attrs["kute_version"] == __version__
            assert f["information"].attrs["author"] == getpass.getuser()
            assert f["information/units"].attrs["time"] == "ps"
            assert f["information/units"].attrs["electric_current"] == "e * A / ps"

            # Check for correct shapes

            assert len(np.array(f["timeseries/time"])) == TOTALSTEPS
            assert np.array(f["timeseries/current"]).shape == (TOTALSTEPS, 3)

        os.remove(FILEPATH)

class TestCOMVelocityReporter(object):

    @pytest.mark.skipif(SKIP_TESTS, reason="OpenMM is not installed")
    def test_reporter(self, simulation):

        simulation.reporters.clear()
        
        current_reporter = COMVelocityReporter(os.path.join(ACTUAL_PATH, "report_com_vel_temp.h5"), reportInterval=1)
        simulation.reporters.append(current_reporter)

        simulation.step(TOTALSTEPS)

        # To close the reporter object
        simulation.reporters.clear()
        del current_reporter

        # Check if report exists

        FILEPATH = os.path.join(ACTUAL_PATH, "report_com_vel_temp.h5")
        assert os.path.isfile(FILEPATH)

        # Check if it can be loaded with KUTE

        names = np.unique([r.name for r in simulation.topology.residues()])
        for name in names:
            t, Vx, Vy, Vz = load_com_velocity(FILEPATH, name)
            number = np.sum([ 1 if r.name==name else 0 for r in simulation.topology.residues() ])
            assert Vx.shape == (number, len(t))
            assert Vy.shape == (number, len(t))
            assert Vz.shape == (number, len(t))

        # Checks for the h5 file

        with h5py.File(FILEPATH) as f:

            # General information

            assert f["information"].attrs["kute_version"] == __version__
            assert f["information"].attrs["author"] == getpass.getuser()
            assert f["information/units"].attrs["time"] == "ps"
            assert f["information/units"].attrs["com_velocities"] == "A / ps"

            # Check residue counts

            for name in names:

                number = np.sum([ 1 if r.name==name else 0 for r in simulation.topology.residues() ])
                assert len(np.array(f[f"residues/{name}"])) == number

            # Check the shape of the results
            
            target_shape = (TOTALSTEPS, simulation.topology.getNumResidues(), 3)

            assert len(np.array(f["timeseries/time"])) == TOTALSTEPS
            assert np.array(f["timeseries/com_velocities"]).shape == target_shape

        
        os.remove(FILEPATH)

class TestPressureTensorReporter(object):

    @pytest.mark.skipif(SKIP_TESTS, reason="OpenMM is not installed")
    def test_reporter(self, simulation):

        simulation.reporters.clear()
        
        current_reporter = PressureTensorReporter(os.path.join(ACTUAL_PATH, "report_pressure_tensor_temp.h5"), reportInterval=1)
        simulation.reporters.append(current_reporter)

        simulation.step(TOTALSTEPS)

        # To close the reporter object
        simulation.reporters.clear()
        del current_reporter

        # Check if report exists

        FILEPATH = os.path.join(ACTUAL_PATH, "report_pressure_tensor_temp.h5")
        assert os.path.isfile(FILEPATH)

        ## Check if the file can be loaded with KUTE

        t, Pxy, Pxz, Pyz = load_pressure_tensor(FILEPATH)
        
        assert Pxy.shape == (1, len(t))
        assert Pxz.shape == (1, len(t))
        assert Pyz.shape == (1, len(t))

        # Checks for the h5 file

        with h5py.File(FILEPATH, "r") as f:

            # Check general information

            assert f["information"].attrs["kute_version"] == __version__
            assert f["information"].attrs["author"] == getpass.getuser()
            assert f["information/units"].attrs["time"] == "ps"
            assert f["information/units"].attrs["pressure_tensor"] == "Pa"

            # Check for correct shapes

            assert len(np.array(f["timeseries/time"])) == TOTALSTEPS
            assert np.array(f["timeseries/pressure_tensor"]).shape == (TOTALSTEPS, 3)

        os.remove(FILEPATH)