# Copyright (c) 2024 The KUTE contributors

import getpass

import h5py
from MDAnalysis import Universe
from ._kuteanalysis import KuteAnalysis
import numpy as np

from kute import __version__

class COMVelocity(KuteAnalysis):
    """
    Class to calculate center of mass velocities from MD trajectories.

    Args:
        universe (MDAnalysis.Universe): Universe containig the simulation
        filename (str, optional): Name of the h5 file to which the velocities will be saved. 
                                  Defaults to "com_velocity.h5".
    """

    _analysis_algorithm_is_parallelizable = True

    def __init__(self, universe: Universe, filename:str="com_velocity.h5", **kwargs):

        super().__init__(universe.trajectory, **kwargs)
        
        self.u = universe
        self.filename = filename
        
        weights = self.u.atoms.masses / np.array([ a.residue.mass for a in self.u.atoms ])
        self._matrix = np.zeros((self.u.residues.n_residues, self.u.atoms.n_atoms))

        for i, res in enumerate(self.u.residues):
            for atom in res.atoms:
                j = atom.index
                self._matrix[i, j] = weights[j]
        
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

        self.results.com_vel = np.zeros((self.n_frames, self.u.residues.n_residues, 3))

    def _single_frame(self):

        self.results.com_vel[self._frame_index, :, :] = self._matrix @ self.u.atoms.velocities
    
    def _conclude(self):

        self.write_h5_file()

    def _get_aggregator(self):
        from MDAnalysis.analysis.base import ResultsGroup
        return ResultsGroup(lookup={'com_vel': ResultsGroup.ndarray_vstack})

    def write_h5_file(self):

        with h5py.File(self.filename, "w") as file:

        ## Metadata group

            file.create_group('information')
            file['information'].attrs['kute_version'] = __version__
            file['information'].attrs['author'] = getpass.getuser()
            file['information'].create_group('units')
            file['information/units'].attrs['time'] = "ps"
            file['information/units'].attrs['com_velocities'] = "A / ps"

            ## Residue identificators

            file.create_group('residues')
            names = self.u.residues.resnames
            for name in np.unique(names):
                where = np.where(names==name)[0]
                file['residues'].create_dataset(name, data=where, dtype=int)

            ## Data group

            file.create_group('timeseries')
            file['timeseries'].create_dataset('time', data=self.times, maxshape=(None,))
            file['timeseries'].create_dataset('com_velocities', data=self.results.com_vel, maxshape=(None, self.u.residues.n_residues, 3))