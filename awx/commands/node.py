"""Awx node helper module."""
from ..base import AwxBase

# TODO: Add in additional parameters that are optional for all methods.


class AwxNode(AwxBase):
    """Awx node class."""
    __resource_name__ = 'node'

    def __init__(self):
        """Constructor."""
        super(AwxNode, self).__init__()
