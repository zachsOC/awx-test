"""Awx workflow helper module."""
from ..base import AwxBase

# TODO: Add in additional parameters that are optional for all methods.


class AwxWorkflow(AwxBase):
    """Awx workflow class."""
    __resource_name__ = 'workflow'

    def __init__(self):
        """Constructor."""
        super(AwxWorkflow, self).__init__()
