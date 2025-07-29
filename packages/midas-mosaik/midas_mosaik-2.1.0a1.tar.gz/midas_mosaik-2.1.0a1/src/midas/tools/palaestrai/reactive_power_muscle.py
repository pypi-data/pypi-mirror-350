import logging
from warnings import warn

from midas_palaestrai.reactive_power_muscle import ReactivePowerMuscle

LOG = logging.getLogger(__name__)

msg = (
    "Importing from 'midas.tools.palaestrai' is deprecated! "
    "Use 'midas_palaestrai' instead!"
)
warn(msg, DeprecationWarning, 2)
LOG.warning(msg)
