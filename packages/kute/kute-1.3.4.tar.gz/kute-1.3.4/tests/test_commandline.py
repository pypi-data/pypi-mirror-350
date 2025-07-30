# Copyright (c) 2024 The KUTE contributors

import sys
import os

import h5py
import MDAnalysis as mda
import numpy as np
import pytest

import kute.__main__

try:
    import dask
    SKIP_DASK = False
except ImportError:
    SKIP_DASK = True

ACTUAL_PATH = os.path.split(os.path.join(os.path.abspath(__file__)))[0]

@pytest.fixture
def microscopic_current_file(property):
    equivalences = {"electric_conductivity":  os.path.join(ACTUAL_PATH, "files_for_tests/inputs/current_test.h5"),
                    "diffusion_coefficient": os.path.join(ACTUAL_PATH, "files_for_tests/inputs/com_velocity_test.h5"),
                    "viscosity": os.path.join(ACTUAL_PATH, "files_for_tests/inputs/pressure_tensor_test.h5")}
    
    return equivalences[property]


@pytest.fixture
def property(property_name):
    return property_name


class TestCalculateTransportCoefficientRoutine(object):

    @pytest.mark.parametrize("property_name,resname", [("electric_conductivity", None), ("diffusion_coefficient", "ea"), ("diffusion_coefficient", "no3"),("viscosity", None)])
    def test_loader_functions(self, property, microscopic_current_file, resname):
        
        from kute.routines._calculate_transport_coefficient import get_loader_function

        loader = get_loader_function(property, resname)
        t, Jx, Jy, Jz = loader(microscopic_current_file, 1)


    @pytest.mark.parametrize("property_name", ["electric_conductivity", "diffusion_coefficient", "viscosity"])
    @pytest.mark.parametrize("splits", [1, 2, 4])
    @pytest.mark.parametrize("resname", ["ea", "no3"])
    def test_calculation_for_one(self, property, microscopic_current_file, resname, splits):
        
        from kute.routines._calculate_transport_coefficient import calculation_for_one
        from kute.routines._calculate_transport_coefficient import get_loader_function    

        loader = get_loader_function(property, resname)

        ## Create random weight for the test

        weight = np.array(np.random.random((1,1)))
        np.savetxt("weight_temp.dat", weight)

        t, avg, uavg = calculation_for_one(microscopic_current_file, loader, splits, "weight_temp.dat")

        assert len(t) == len(avg)
        assert len(avg) == len(uavg)

        os.remove("weight_temp.dat")


    @pytest.mark.parametrize("property_name", ["electric_conductivity", "diffusion_coefficient", "viscosity"])
    @pytest.mark.parametrize("splits", [1, 2, 4])
    @pytest.mark.parametrize("resname", ["ea", "no3"])
    @pytest.mark.parametrize("repetitions", [2, 3])
    def test_calculation_for_ensemble(self, property, microscopic_current_file, resname, splits, repetitions):

        from kute.routines._calculate_transport_coefficient import calculation_for_ensemble
        from kute.routines._calculate_transport_coefficient import get_loader_function

        loader = get_loader_function(property, resname)

        weight = np.random.random(repetitions) 
        np.savetxt("weight_temp.dat", weight)

        t, avg, uavg = calculation_for_ensemble([microscopic_current_file for _ in range(repetitions)], loader, splits, "weight_temp.dat")

        assert len(t) == len(avg)
        assert len(avg) == len(uavg)

        os.remove("weight_temp.dat")

    @pytest.mark.parametrize("number", [100, 500, 1000])
    def test_save_results(self, number):
    
        from kute.routines._calculate_transport_coefficient import save_results

        t, avg, uavg = np.random.random((3, number))
        save_results("temporal.dat", t, avg, uavg)

        assert os.path.isfile("temporal.dat")

        os.remove("temporal.dat")

    @pytest.mark.parametrize("property_name", ["electric_conductivity", "diffusion_coefficient", "viscosity"])
    @pytest.mark.parametrize("splits", [1, 2, 4])
    @pytest.mark.parametrize("resname", ["ea", "no3"])
    @pytest.mark.parametrize("repetitions", [2, 3])
    def test_commandline_routine(self, microscopic_current_file, property, splits, repetitions, resname):
        
        file_list = " ".join([microscopic_current_file for _ in range(repetitions)])
        command = f"kute calculate_transport_coefficient -f {file_list} --splits {splits} --output temporary_out.dat --resname {resname} --property {property}"

        sys.argv = command.split()
        kute.__main__.main()

        assert os.path.isfile("temporary_out.dat")
        os.remove("temporary_out.dat")


@pytest.fixture
def trajectory_file():
    return os.path.join(ACTUAL_PATH, "files_for_tests/inputs/traj.trr")

@pytest.fixture
def topology_file():
    return os.path.join(ACTUAL_PATH, "files_for_tests/inputs/topo.tpr")

class TestCalculateMicroscopicCurrentRoutine(object):

    @pytest.mark.parametrize("current_type", ["electric_current", "com_velocity", "pressure_tensor"])
    def test_get_analysis_class(self, current_type):

        from kute.routines._calculate_microscopic_current import get_analysis_class

        analysis_class = get_analysis_class(current_type)

    @pytest.mark.parametrize("current_type", ["electric_current", "com_velocity", "pressure_tensor"])
    @pytest.mark.parametrize('backend', [
                                        'serial', 
                                        'multiprocessing', 
                                        pytest.param('dask', marks=pytest.mark.skipif(SKIP_DASK, reason="Dask is not installed"))
                                        ])
    def test_perform_analysis(self, trajectory_file, topology_file, current_type, backend):

        from kute.routines._calculate_microscopic_current import get_analysis_class, perform_analysis

        u = mda.Universe(topology_file, trajectory_file)
        analysis_class = get_analysis_class(current_type)

        perform_analysis(u, analysis_class, "temporary_out.h5", backend=backend, n_workers=2)

        assert os.path.isfile("temporary_out.h5")
        os.remove("temporary_out.h5")


    @pytest.mark.parametrize("current_type", ["electric_current", "com_velocity", "pressure_tensor"])
    @pytest.mark.parametrize('backend', [
                                        'serial', 
                                        'multiprocessing', 
                                        pytest.param('dask', marks=pytest.mark.skipif(SKIP_DASK, reason="Dask is not installed"))
                                        ])
    def test_commandline_routine(self, trajectory_file, topology_file, current_type, backend):

        command = f"kute calculate_microscopic_current --current {current_type} --traj {trajectory_file} --top {topology_file} --output temporary_out.h5 --backend {backend} --n_workers 2"

        sys.argv = command.split()
        kute.__main__.main()

        assert os.path.isfile("temporary_out.h5")
        os.remove("temporary_out.h5")


@pytest.fixture
def current_file(prop):
    equivs = {"electric_current": os.path.join(ACTUAL_PATH, "files_for_tests/inputs/current_test.h5"),
              "com_velocity": os.path.join(ACTUAL_PATH, "files_for_tests/inputs/com_velocity_test.h5"),
              "pressure_tensor": os.path.join(ACTUAL_PATH, "files_for_tests/inputs/pressure_tensor_test.h5")}
    
    return equivs[prop]


class TestJoinCurrentsRoutine(object):

    @pytest.mark.parametrize("prop", ["electric_current", "com_velocity", "pressure_tensor"])
    @pytest.mark.parametrize("repetitions", [2, 3, 4])
    @pytest.mark.parametrize("CHECK", [True, False])
    def test_join_h5_files(self, repetitions, current_file, CHECK):

        from kute.routines._join_currents import join_h5_files

        file_list = [current_file for _ in range(repetitions)]

        join_h5_files("temporary_out.h5", CHECK, *file_list)

        assert os.path.isfile("temporary_out.h5")

        fold = h5py.File(current_file)
        L_old = len(np.array(fold['timeseries/time']))

        fnew = h5py.File("temporary_out.h5")
        L_new = len(np.array(fnew['timeseries/time']))

        assert L_new == L_old * repetitions
        
        fold.close()
        fnew.close()

        os.remove("temporary_out.h5")

    @pytest.mark.parametrize("prop", ["electric_current", "com_velocity", "pressure_tensor"])
    @pytest.mark.parametrize("repetitions", [2, 3, 4])
    @pytest.mark.parametrize("CHECK", [True, False])
    def test_commandline_routine(self, repetitions, current_file, CHECK):

        file_list =" ".join([current_file for _ in range(repetitions)])
        command = f"kute join_currents -f {file_list} -o temporary_out.h5"
        if CHECK:
            command += " --ignore_checks"

        sys.argv = command.split()
        kute.__main__.main()

        assert os.path.isfile("temporary_out.h5")
        os.remove("temporary_out.h5")