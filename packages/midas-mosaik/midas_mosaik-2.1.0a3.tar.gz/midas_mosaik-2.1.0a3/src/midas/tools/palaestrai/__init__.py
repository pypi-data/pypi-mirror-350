import logging
from warnings import warn

from midas_palaestrai.descriptor import Descriptor

try:
    from midas_palaestrai.arl_attacker_objective import ArlAttackerObjective
    from midas_palaestrai.arl_defender_objective import ArlDefenderObjective
    from midas_palaestrai.descriptor import Descriptor
    from midas_palaestrai.reactive_power_muscle import ReactivePowerMuscle
    from midas_palaestrai.voltage_attacker_objective import (
        VoltageBandViolationPendulum,
    )
    from midas_palaestrai.voltage_defender_objective import (
        VoltageDefenderObjective,
    )
except ModuleNotFoundError:
    # palaestrAI might not be installed when, e.g. only the descriptor
    # is used
    pass

LOG = logging.getLogger(__name__)

msg = (
    "Importing from 'midas.tools.palaestrai' is deprecated! "
    "Use 'midas_palaestrai' instead!"
)
warn(msg, DeprecationWarning, 2)
LOG.warning(msg)
