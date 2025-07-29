import logging
from warnings import warn

from midas_palaestrai.rewards import (
    AllesDestroyAllPire2RewardIchWeissNicht,
    ExtendedGridHealthReward,
    GridHealthReward,
    NoExtGridHealthReward,
    RetroPsiReward,
    VoltageBandDeviationReward,
    VoltageBandReward,
)

LOG = logging.getLogger(__name__)

msg = (
    "Importing from 'midas.tools.palaestrai' is deprecated! "
    "Use 'midas_palaestrai' instead!"
)
warn(msg, DeprecationWarning, 2)
LOG.warning(msg)
