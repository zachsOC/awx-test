"""Awx label helper module."""
from ..base import AwxBase

# TODO: Add in additional parameters that are optional for all methods.


class AwxLabel(AwxBase):
    """Awx label class."""
    __resource_name__ = 'label'

    def __init__(self):
        """Constructor."""
        super(AwxLabel, self).__init__()
