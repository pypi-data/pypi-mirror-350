# Copyright (c) 2024 The KUTE contributors
import os 
import pytest
import numpy as np

from kute import GreenKuboIntegral, IntegralEnsemble
from itertools import chain, combinations
from kute.loaders import load_electric_current

ACTUAL_PATH = os.path.split(os.path.join(os.path.abspath(__file__)))[0]




@pytest.fixture
def integral_ensemble(splits, replicas):

    file = os.path.join(ACTUAL_PATH, "files_for_tests/inputs/current_test.h5")
    integrals = [GreenKuboIntegral(*load_electric_current(file, splits)) for _ in range(replicas)]

    return IntegralEnsemble(integrals)


class TestIntegralEnsemble(object):

    @pytest.mark.parametrize("splits,replicas", [(1, 2), (1, 5), (1, 10), (5, 2), (5, 5), (5, 10)])
    def test_load(self, integral_ensemble, replicas):

        assert integral_ensemble.N_REPLICAS == replicas

    @pytest.mark.parametrize("splits,replicas", [(1, 2), (1, 5), (1, 10), (5, 2), (5, 5), (5, 10)])
    def test_calculation(self, integral_ensemble):

        def capped_powerset(iterable):
            """Returns the set of all sets in the iterable that contain at least two elements
            """
            s = list(iterable)
            return list(chain.from_iterable(combinations(s, r) for r in range(2, len(s)+1)))

        keys = ["11", "22", "33", "12", "13", "23"]

        for key_set in capped_powerset(keys):

            t, avg, uavg = integral_ensemble.get_average_over_components(key_set)

            assert avg.shape == uavg.shape
            assert t.shape == avg.shape

    @pytest.mark.parametrize("splits,replicas", [(1, 2), (1, 5), (1, 10), (5, 2), (5, 5), (5, 10)])
    def test_specific_calculations(self, integral_ensemble):

        _, _, _ = integral_ensemble.get_isotropic_average()
        _, _, _ = integral_ensemble.get_anisotropic_average()