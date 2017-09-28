"""Awx permission helper module."""
from ..base import AwxBase

# TODO: Add in additional parameters that are optional for all methods.


class AwxPermission(AwxBase):
    """Awx permission class."""
    __resource_name__ = 'permission'

    def __init__(self):
        """Constructor."""
        super(AwxPermission, self).__init__()
