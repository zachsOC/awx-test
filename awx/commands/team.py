"""Awx team helper module."""
from ..base import AwxBase

# TODO: Add in additional parameters that are optional for all methods.


class AwxTeam(AwxBase):
    """Awx team class."""
    __resource_name__ = 'team'

    def __init__(self):
        """Constructor."""
        super(AwxTeam, self).__init__()
