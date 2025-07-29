from niwrap_ants import ants
from niwrap_workbench import workbench
from niwrap_mrtrix3tissue import mrtrix3tissue
from niwrap_mrtrix import mrtrix
from niwrap_fsl import fsl
from niwrap_dcm2niix import dcm2niix
from niwrap_c3d import c3d
from niwrap_greedy import greedy
from niwrap_freesurfer import freesurfer
from niwrap_fastsurfer import fastsurfer
from niwrap_afni import afni
from niwrap_niftyreg import niftyreg
from styxdefs import *  # Reexport styxdefs
from styxdocker import DockerRunner
from styxsingularity import SingularityRunner
from styxgraph import GraphRunner


def use_local(*args, **kwargs):
    """Set the LocalRunner as the global runner."""
    set_global_runner(LocalRunner(*args, **kwargs))


def use_dry(*args, **kwargs):
    """Set the DryRunner as the global runner."""
    set_global_runner(DryRunner(*args, **kwargs))


def use_docker(*args, **kwargs):
    """Set the DockerRunner as the global runner."""
    set_global_runner(DockerRunner(*args, **kwargs))


def use_singularity(*args, **kwargs):
    """Set the SingularityRunner as the global runner."""
    set_global_runner(SingularityRunner(*args, **kwargs))


def use_graph(*args, **kwargs):
    """Set the GraphRunner as the global runner."""
    set_global_runner(GraphRunner(*args, **kwargs))
