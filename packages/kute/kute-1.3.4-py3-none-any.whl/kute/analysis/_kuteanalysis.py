from MDAnalysis.analysis.base import AnalysisBase
from MDAnalysis import __version__
import warnings
from packaging.version import Version

from typing import Iterable

class KuteAnalysis(AnalysisBase):


    def run(
        self,
        start: int = None,
        stop: int = None,
        step: int = None,
        frames: Iterable = None,
        verbose: bool = None,
        n_workers: int = None,
        n_parts: int = None,
        backend = None,
        *,
        unsupported_backend: bool = False,
        progressbar_kwargs=None):


        if Version(__version__) >= Version("2.8.0"):

            super().run(start=start, 
                        stop=stop, 
                        step=step, 
                        frames=frames, 
                        verbose=verbose,
                        n_workers=n_workers,
                        n_parts=n_parts,
                        backend=backend,
                        unsupported_backend=unsupported_backend,
                        progressbar_kwargs=progressbar_kwargs)

        else:
            
            warnings.warn(f"Current MDAnalysis version ({__version__}) does not support parallel analysis. To enable parallel analysis, update to version 2.8.0 or greater. The analysis will still be carried out in serial mode.", category=RuntimeWarning)
            super().run(start=start,
                        stop=stop,
                        step=step,
                        verbose=verbose)