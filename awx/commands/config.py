"""Awx config helper module."""
from ..base import AwxBase

# TODO: Add in additional parameters that are optional for all methods.


class AwxConfig(AwxBase):
    """Awx config class."""
    __resource_name__ = 'config'

    def __init__(self):
        """Constructor."""
        super(AwxConfig, self).__init__()
