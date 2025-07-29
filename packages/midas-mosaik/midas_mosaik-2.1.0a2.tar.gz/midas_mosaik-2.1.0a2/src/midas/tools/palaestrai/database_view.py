import logging
from warnings import warn

from midas_palaestrai.database_view import (
    create_midas_views,
    make_muscle_actions_query,
)

LOG = logging.getLogger(__name__)

msg = (
    "Importing from 'midas.tools.palaestrai' is deprecated! "
    "Use 'midas_palaestrai' instead!"
)
warn(msg, DeprecationWarning, 2)
LOG.warning(msg)
