"""Awx role helper module."""
from ..base import AwxBase

# TODO: Add in additional parameters that are optional for all methods.


class AwxRole(AwxBase):
    """Awx role class."""
    __resource_name__ = 'role'

    def __init__(self):
        """Constructor."""
        super(AwxRole, self).__init__()
