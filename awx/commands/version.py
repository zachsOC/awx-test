"""Awx version helper module."""
from ..base import AwxBase

# TODO: Add in additional parameters that are optional for all methods.


class AwxVersion(AwxBase):
    """Awx version class."""
    __resource_name__ = 'version'

    def __init__(self):
        """Constructor."""
        super(AwxVersion, self).__init__()
