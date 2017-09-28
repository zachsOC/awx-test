"""Awx group helper module."""
from ..base import AwxBase

# TODO: Add in additional parameters that are optional for all methods.


class AwxGroup(AwxBase):
    """Awx group class."""
    __resource_name__ = 'group'

    def __init__(self):
        """Constructor."""
        super(AwxGroup, self).__init__()
