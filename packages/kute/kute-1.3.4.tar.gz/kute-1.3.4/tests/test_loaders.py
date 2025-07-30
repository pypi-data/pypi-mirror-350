# Copyright (c) 2024 The KUTE contributors

import os
import pytest
import h5py
import numpy as np
from kute.loaders import load_com_velocity, load_electric_current, load_pressure_tensor


ACTUAL_PATH = os.path.split(os.path.join(os.path.abspath(__file__)))[0]

@pytest.fixture
def current_h5():
    file = os.path.join(ACTUAL_PATH, "files_for_tests/inputs/current_test.h5")
    return h5py.File(file)

@pytest.fixture
def com_velocity_h5():
    file = os.path.join(ACTUAL_PATH, "files_for_tests/inputs/com_velocity_test.h5")
    return h5py.File(file)

@pytest.fixture
def pressure_tensor_h5():
    file = os.path.join(ACTUAL_PATH, "files_for_tests/inputs/pressure_tensor_test.h5")
    return h5py.File(file)

@pytest.fixture
def current(splits):

    file = os.path.join(ACTUAL_PATH, "files_for_tests/inputs/current_test.h5")
    return load_electric_current(file, splits)

@pytest.fixture
def com_velocity(splits, resname):

    file = os.path.join(ACTUAL_PATH, "files_for_tests/inputs/com_velocity_test.h5")
    return load_com_velocity(file, resname, splits)

@pytest.fixture
def pressure_tensor(splits):
    file = os.path.join(ACTUAL_PATH, "files_for_tests/inputs/pressure_tensor_test.h5")
    return load_pressure_tensor(file, splits)


class TestElectricCurrent(object):

    @pytest.mark.parametrize("splits", [(1)])
    def test_load(self, current_h5, current):

        time, Jx, Jy, Jz = current
        time_h5 = np.array(current_h5["timeseries/time"])
        Jx_h5, Jy_h5, Jz_h5 = np.array(current_h5["timeseries/current"]).T

        assert np.allclose(time, time_h5)
        assert np.allclose(Jx, Jx_h5)
        assert np.allclose(Jy, Jy_h5)
        assert np.allclose(Jz, Jz_h5)
    

    @pytest.mark.parametrize("splits", [1, 2, 5, 10])
    def test_shape(self, current_h5, current, splits):

        time, Jx, Jy, Jz = current
        len_h5 = len(np.array(current_h5["timeseries/time"]))
        target_len = len_h5 / splits

        ## Check for correct splitting of the time
        assert (len(time) == target_len)

        ## Check that all currents have the correct shape

        correct_shape = (splits, target_len)

        assert Jx.shape == correct_shape
        assert Jy.shape == correct_shape
        assert Jz.shape == correct_shape

class TestPressureTensor(object):

    @pytest.mark.parametrize("splits", [(1)])
    def test_load(self, pressure_tensor_h5, pressure_tensor):

        time, Px, Py, Pz = pressure_tensor
        time_h5 = np.array(pressure_tensor_h5["timeseries/time"])
        Px_h5, Py_h5, Pz_h5 = np.array(pressure_tensor_h5["timeseries/pressure_tensor"]).T

        assert np.allclose(time, time_h5)
        assert np.allclose(Px, Px_h5)
        assert np.allclose(Py, Py_h5)
        assert np.allclose(Pz, Pz_h5)

    @pytest.mark.parametrize("splits", [1, 2, 5, 10])
    def test_shape(self, pressure_tensor_h5, pressure_tensor, splits):

        time, Px, Py, Pz = pressure_tensor
        len_h5 = len(np.array(pressure_tensor_h5["timeseries/time"]))
        target_len = len_h5 / splits

        ## Check for correct splitting of the time
        assert (len(time) == target_len)

        ## Check that all currents have the correct shape

        correct_shape = (splits, target_len)

        assert Px.shape == correct_shape
        assert Py.shape == correct_shape
        assert Pz.shape == correct_shape


class TestCOMVelocity(object):

    @pytest.mark.parametrize("splits,resname", [(1, "ea"), (1, "no3"), (2, "ea"), (2, "no3"), (5, "ea"), (5, "no3"), (10, "ea"), (10, "no3")])
    def test_load(self, com_velocity_h5, com_velocity, splits, resname):


        time, Vx, Vy, Vz = com_velocity
        time_h5 = np.array(com_velocity_h5["timeseries/time"])
        
        if resname == "ea":
            Vx_h5, Vy_h5, Vz_h5 = np.split(np.array(com_velocity_h5["timeseries/com_velocities"]), 2, axis=1)[0].T

        elif resname == "no3":
            Vx_h5, Vy_h5, Vz_h5 = np.split(np.array(com_velocity_h5["timeseries/com_velocities"]), 2, axis=1)[1].T

        Vx_h5 = np.vstack(np.split(Vx_h5, splits, axis=1))
        Vy_h5 = np.vstack(np.split(Vy_h5, splits, axis=1))
        Vz_h5 = np.vstack(np.split(Vz_h5, splits, axis=1))

        assert np.allclose(time, time_h5[:len(time_h5)//splits])
        assert np.allclose(Vx, Vx_h5)
        assert np.allclose(Vy, Vy_h5)
        assert np.allclose(Vz, Vz_h5)

    @pytest.mark.parametrize("splits", [1, 5, 10])
    def test_missing_residue(self, splits):
        with pytest.raises(ValueError):
            _, _, _, _ = load_com_velocity(os.path.join(ACTUAL_PATH, "files_for_tests/inputs/com_velocity_test.h5"), "missing", splits)


    @pytest.mark.parametrize("splits,resname", [(1, "ea"), (1, "no3"), (2, "ea"), (2, "no3"), (5, "ea"), (5, "no3"), (10, "ea"), (10, "no3")])
    def test_shape(self, com_velocity_h5, com_velocity, splits, resname):

        _, Vx, Vy, Vz = com_velocity
        time_h5 = np.array(com_velocity_h5["timeseries/time"])

        n_residues = len(np.array(com_velocity_h5[f"residues/{resname}"]))

        time_h5 = time_h5[:len(time_h5)//splits]
        target_shape = (n_residues * splits, len(time_h5))

        assert Vx.shape == target_shape
        assert Vy.shape == target_shape
        assert Vz.shape == target_shape

