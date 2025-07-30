# Copyright (c) 2024 The KUTE contributors

import os 
import pytest
import numpy as np

from kute import GreenKuboIntegral
from kute.loaders import load_electric_current
from itertools import chain, combinations

ACTUAL_PATH = os.path.split(os.path.join(os.path.abspath(__file__)))[0]

@pytest.fixture
def current(splits):
    file = os.path.join(ACTUAL_PATH, "files_for_tests/inputs/current_test.h5")
    return load_electric_current(file, splits)

@pytest.fixture
def green_kubo_integral(splits):
    file = os.path.join(ACTUAL_PATH, "files_for_tests/inputs/current_test.h5")
    return GreenKuboIntegral(*load_electric_current(file, splits))

@pytest.fixture
def results_correlation():
    file = os.path.join(ACTUAL_PATH, "files_for_tests/results/results_correlation_test.dat")
    c11, c22, c33, c12, c13, c23 = np.loadtxt(file).T
    return c11, c22, c33, c12, c13, c23 

@pytest.fixture
def uncertainty_correlation():
    file = os.path.join(ACTUAL_PATH, "files_for_tests/results/uncertainty_correlation_test.dat")
    uc11, uc22, uc33, uc12, uc13, uc23 = np.loadtxt(file).T
    return uc11, uc22, uc33, uc12, uc13, uc23 

@pytest.fixture
def results_integral():
    file = os.path.join(ACTUAL_PATH, "files_for_tests/results/results_integral_test.dat")
    c11, c22, c33, c12, c13, c23 = np.loadtxt(file).T
    return c11, c22, c33, c12, c13, c23 

@pytest.fixture
def uncertainty_integral():
    file = os.path.join(ACTUAL_PATH, "files_for_tests/results/uncertainty_integral_test.dat")
    uc11, uc22, uc33, uc12, uc13, uc23 = np.loadtxt(file).T
    return uc11, uc22, uc33, uc12, uc13, uc23 

@pytest.fixture
def results_running_average():
    file = os.path.join(ACTUAL_PATH, "files_for_tests/results/results_running_average_test.dat")
    c11, c22, c33, c12, c13, c23 = np.loadtxt(file).T
    return c11, c22, c33, c12, c13, c23 

@pytest.fixture
def uncertainty_running_average():
    file = os.path.join(ACTUAL_PATH, "files_for_tests/results/uncertainty_running_average_test.dat")
    uc11, uc22, uc33, uc12, uc13, uc23 = np.loadtxt(file).T
    return uc11, uc22, uc33, uc12, uc13, uc23 

@pytest.fixture
def results_isotropic():
    file = os.path.join(ACTUAL_PATH, "files_for_tests/results/results_isotropic_test.dat")
    t, avg, uavg = np.loadtxt(file).T
    return t, avg, uavg

@pytest.fixture
def results_anisotropic():
    file = os.path.join(ACTUAL_PATH, "files_for_tests/results/results_anisotropic_test.dat")
    t, avg, uavg = np.loadtxt(file).T
    return t, avg, uavg

class TestGreenKuboIntegral(object):

    @pytest.mark.parametrize("splits", [1, 2, 5, 10])
    def test_load(self, green_kubo_integral, current):

        integral = green_kubo_integral
        t, Jx, Jy, Jz = current

        assert np.allclose(integral.time, t)
        assert np.allclose(integral.J1, Jx)
        assert np.allclose(integral.J2, Jy)
        assert np.allclose(integral.J3, Jz)

        assert not integral._calculated_caf
        assert not integral._calculated_integral
        assert not integral._calculated_running_average

    @pytest.mark.parametrize("splits", [1, 2, 5, 10])
    def test_set_time_to_zero(self, green_kubo_integral):

        integral = green_kubo_integral
        integral.time += 10
        integral.set_time_to_zero()
        assert integral.time[0] == 0

    @pytest.mark.parametrize("splits", [1])
    def test_get_correlation_function(self, green_kubo_integral):

        j1 = np.random.random((10, 100))        
        j2 = np.random.random((11, 100))

        with pytest.raises(ValueError):
            _ = green_kubo_integral.get_correlation_function(j1, j2)

        j1 = np.random.random((5, 50))
        j2 = np.random.random((5, 50))

        results = green_kubo_integral.get_correlation_function(j1, j2)

        assert results.shape == (49, 2)

        j1 = np.random.random(50)
        j2 = np.random.random(50)

        results = green_kubo_integral.get_correlation_function(j1, j2)

        assert results.shape == (49, 2)

    @pytest.mark.parametrize("splits", [1])
    def test_analysis_sequence(self, green_kubo_integral):

        with pytest.raises(RuntimeError):
            green_kubo_integral._calculated_caf = False
            green_kubo_integral._calculate_integral()
        with pytest.raises(RuntimeError):
            green_kubo_integral._calculated_caf = False
            green_kubo_integral._calculated_integral = False
            green_kubo_integral._calculate_running_average()
        with pytest.raises(RuntimeError):
            green_kubo_integral._calculated_caf = True
            green_kubo_integral._calculated_integral = False
            green_kubo_integral._calculate_running_average()
        with pytest.raises(RuntimeError):
            green_kubo_integral._calculated_caf = False
            green_kubo_integral._calculated_integral = True
            green_kubo_integral._calculate_running_average()



    @pytest.mark.parametrize("splits", [1])
    def test_calculate_correlation(self, green_kubo_integral, results_correlation, uncertainty_correlation):

        integral = green_kubo_integral
        integral._calculate_correlation()

        assert integral._calculated_caf

        c11, c22, c33, c12, c13, c23 = results_correlation
        uc11, uc22, uc33, uc12, uc13, uc23 = uncertainty_correlation

        # Assert the values

        assert np.allclose(c11, integral.caf["11"][:, 0])
        assert np.allclose(c22, integral.caf["22"][:, 0])
        assert np.allclose(c33, integral.caf["33"][:, 0])
        assert np.allclose(c12, integral.caf["12"][:, 0])
        assert np.allclose(c13, integral.caf["13"][:, 0])
        assert np.allclose(c23, integral.caf["23"][:, 0])

        # Assert the uncertainties

        assert np.allclose(uc11, integral.caf["11"][:, 1])
        assert np.allclose(uc22, integral.caf["22"][:, 1])
        assert np.allclose(uc33, integral.caf["33"][:, 1])
        assert np.allclose(uc12, integral.caf["12"][:, 1])
        assert np.allclose(uc13, integral.caf["13"][:, 1])
        assert np.allclose(uc23, integral.caf["23"][:, 1])

    @pytest.mark.parametrize("splits", [1])
    def test_calculate_integral(self, green_kubo_integral, results_integral, uncertainty_integral):

        integral = green_kubo_integral
        integral._calculate_correlation()
        assert integral._calculated_caf
        integral._calculate_integral()
        assert integral._calculated_integral

        c11, c22, c33, c12, c13, c23 = results_integral
        uc11, uc22, uc33, uc12, uc13, uc23 = uncertainty_integral

        # Assert the values

        assert np.allclose(c11, integral.cumulative_integral["11"][:, 0])
        assert np.allclose(c22, integral.cumulative_integral["22"][:, 0])
        assert np.allclose(c33, integral.cumulative_integral["33"][:, 0])
        assert np.allclose(c12, integral.cumulative_integral["12"][:, 0])
        assert np.allclose(c13, integral.cumulative_integral["13"][:, 0])
        assert np.allclose(c23, integral.cumulative_integral["23"][:, 0])

        # Assert the uncertainties

        assert np.allclose(uc11, integral.cumulative_integral["11"][:, 1])
        assert np.allclose(uc22, integral.cumulative_integral["22"][:, 1])
        assert np.allclose(uc33, integral.cumulative_integral["33"][:, 1])
        assert np.allclose(uc12, integral.cumulative_integral["12"][:, 1])
        assert np.allclose(uc13, integral.cumulative_integral["13"][:, 1])
        assert np.allclose(uc23, integral.cumulative_integral["23"][:, 1])

    @pytest.mark.parametrize("splits", [1])
    def test_calculate_running_average(self, green_kubo_integral, results_running_average, uncertainty_running_average):

        integral = green_kubo_integral
        integral._calculate_correlation()
        assert integral._calculated_caf
        integral._calculate_integral()
        assert integral._calculated_integral
        integral._calculate_running_average()
        assert integral._calculated_running_average

        c11, c22, c33, c12, c13, c23 = results_running_average
        uc11, uc22, uc33, uc12, uc13, uc23 = uncertainty_running_average

        # Assert the values

        assert np.allclose(c11, integral.running_average["11"][:, 0])
        assert np.allclose(c22, integral.running_average["22"][:, 0])
        assert np.allclose(c33, integral.running_average["33"][:, 0])
        assert np.allclose(c12, integral.running_average["12"][:, 0])
        assert np.allclose(c13, integral.running_average["13"][:, 0])
        assert np.allclose(c23, integral.running_average["23"][:, 0])

        # Assert the uncertainties

        assert np.allclose(uc11, integral.running_average["11"][:, 1])
        assert np.allclose(uc22, integral.running_average["22"][:, 1])
        assert np.allclose(uc33, integral.running_average["33"][:, 1])
        assert np.allclose(uc12, integral.running_average["12"][:, 1])
        assert np.allclose(uc13, integral.running_average["13"][:, 1])
        assert np.allclose(uc23, integral.running_average["23"][:, 1])

    
    @pytest.mark.parametrize("splits", [1, 2, 5, 10])
    def test_analyze(self, green_kubo_integral):

        green_kubo_integral.analyze()
        assert green_kubo_integral._calculated_caf
        assert green_kubo_integral._calculated_integral
        assert green_kubo_integral._calculated_running_average


    @pytest.mark.parametrize("splits", [1])
    def test_isotropic_conductivity(self, green_kubo_integral, results_isotropic):

        green_kubo_integral.analyze()

        for v1, v2 in zip(results_isotropic, green_kubo_integral.get_isotropic_running_average()):

            assert np.allclose(v1, v2)

    @pytest.mark.parametrize("splits", [1])
    def test_anisotropic_conductivity(self, green_kubo_integral, results_anisotropic):

        green_kubo_integral.analyze()
        
        for v1, v2 in zip(results_anisotropic, green_kubo_integral.get_anisotropic_running_average()):

            assert np.allclose(v1, v2)

    @pytest.mark.parametrize("splits", [1, 2, 5, 10])
    def test_get_average_correlation_function(self, green_kubo_integral):


        def powerset(iterable):
            """Returns the set of all sets in the iterable
            """
            s = list(iterable)
            return list(chain.from_iterable(combinations(s, r) for r in range(1, len(s)+1)))

        keys = ["11", "22", "33", "12", "13", "23"]

        for key_set in powerset(keys):

            t, avg, unc = green_kubo_integral.get_average_correlation_function(key_set)

            assert t.shape == avg.shape
            assert avg.shape == unc.shape

    @pytest.mark.parametrize("splits", [1, 2, 5, 10])
    def test_specific_correlations(self, green_kubo_integral):

        _, _ , _ = green_kubo_integral.get_isotropic_correlation_function()
        _, _ , _ = green_kubo_integral.get_anisotropic_correlation_function()
       


        
    