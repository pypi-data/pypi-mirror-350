# Copyright (c) 2024 The KUTE contributors

import numpy as np
import h5py
import getpass

from kute import __version__
from ._kuteanalysis import KuteAnalysis
from MDAnalysis import Universe

class ElectricCurrent(KuteAnalysis):
    """
    Class to calculate electric currents from MD trajectories.

    Args:
        universe (MDAnalysis.Universe): Universe containig the simulation
        filename (str, optional): Name of the h5 file to which the current will be saved. 
                                  Defaults to "current.h5".
    """

    _analysis_algorithm_is_parallelizable = True
    
    def __init__(self, universe: Universe, filename: str="current.h5", **kwargs):

        super().__init__(universe.trajectory, **kwargs)
        
        self.u = universe
        self.filename = filename

        residue_masses = np.array([ a.residue.mass for a in self.u.atoms ])
        residue_charges = np.array([ a.residue.charge for a in self.u.atoms ])

        self._weights = residue_charges * self.u.atoms.masses / residue_masses

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
             
        self.results.current = np.zeros((self.n_frames, 3))

    def _single_frame(self):

        self.results.current[self._frame_index, :] = np.sum(self.u.atoms.velocities * self._weights[:, np.newaxis], axis=0)

    def _conclude(self):

        self.write_h5_file()

    def _get_aggregator(self):
        from MDAnalysis.analysis.base import ResultsGroup
        return ResultsGroup(lookup={'current': ResultsGroup.ndarray_vstack})

    def write_h5_file(self):
        """
        Write the current to an h5 file
        """

        with h5py.File(self.filename, "w") as file:

            ## Metadata group

            file.create_group('information')
            file['information'].attrs['kute_version'] = __version__
            file['information'].attrs['author'] = getpass.getuser()
            file['information'].create_group('units')
            file['information/units'].attrs['time'] = "ps"
            file['information/units'].attrs['electric_current'] = "e * A / ps"

            ## Data group

            file.create_group('timeseries')
            file['timeseries'].create_dataset('time', data = self.times, maxshape=(None,))
            file['timeseries'].create_dataset('current', data = self.results.current, maxshape=(None, 3))
