# Copyright (c) 2024 The KUTE contributors

import numpy as np
import h5py
import getpass

from kute import __version__
from ._kuteanalysis import KuteAnalysis
from MDAnalysis import Universe

class PressureTensor(KuteAnalysis):
    """
    Class to calculate the off diagonal components of the pressure tensor from MD trajectories.

    Args:
        universe (MDAnalysis.Universe): Universe containig the simulation
        filename (str, optional): Name of the h5 file to which the pressure will be saved. 
                                  Defaults to "pressure_tensor.h5".
    """

    _analysis_algorithm_is_parallelizable = True

    def __init__(self, universe: Universe, filename: str="pressure_tensor.h5", **kwargs):

        super().__init__(universe.trajectory, **kwargs)

        self.u = universe
        self.filename = filename

    @classmethod
    def get_supported_backends(cls):
        """Tuple with backends supported by the core library for a given class.
        User can pass either one of these values as ``backend=...`` to
        :meth:`run()` method, or a custom object that has ``apply`` method
        (see documentation for :meth:`run()`):

         - 'serial': no parallelization
         - 'multiprocessing': parallelization using `multiprocessing.Pool`
         - 'dask': parallelization using `dask.delayed.compute()`. Requires
           installation of `mdanalysis[dask]`

        If you want to add your own backend to an existing class, pass a
        :class:`backends.BackendBase` subclass (see its documentation to learn
        how to implement it properly), and specify ``unsupported_backend=True``.

        Returns
        -------
        tuple
            names of built-in backends that can be used in :meth:`run(backend=...)`


        .. versionadded:: 1.3.0
        """
        return ('serial', 'multiprocessing', 'dask',)
    
    def _prepare(self):

        self.results.off_diagonal = np.zeros((self.n_frames, 3))

    def _single_frame(self):
        
        positions = self.u.atoms.positions * 1e-10
        velocities = self.u.atoms.velocities * 1e-10 / 1e-12
        forces = self.u.atoms.forces * 1e3 / (1e-10 * 6.02214076e23)
        volume = self.u.dimensions[:3].prod() * 1e-30

        m_v_v_tensor = 1.66054e-27 * np.tensordot(self.u.atoms.masses[:, np.newaxis]*velocities, velocities, axes=(0, 0))

        r_f_tensor = np.tensordot(positions, forces, axes=(0, 0))

        tensor = np.triu(m_v_v_tensor + r_f_tensor, k=1)

        self.results.off_diagonal[self._frame_index, :] = tensor.flatten()[np.flatnonzero(tensor)] / volume

    def _conclude(self):

        self.write_h5_file()

    def _get_aggregator(self):
        from MDAnalysis.analysis.base import ResultsGroup
        return ResultsGroup(lookup={'off_diagonal': ResultsGroup.ndarray_vstack})
    
    def write_h5_file(self):
        """
        Write the pressure to an h5 file
        """

        with h5py.File(self.filename, "w") as file:

            ## Metadata group

            file.create_group('information')
            file['information'].attrs['kute_version'] = __version__
            file['information'].attrs['author'] = getpass.getuser()
            file['information'].create_group('units')
            file['information/units'].attrs['time'] = "ps"
            file['information/units'].attrs['pressure_tensor'] = "Pa"

            ## Data group

            file.create_group('timeseries')
            file['timeseries'].create_dataset('time', data = self.times, maxshape=(None,))
            file['timeseries'].create_dataset('pressure_tensor', data = self.results.off_diagonal, maxshape=(None, 3))
