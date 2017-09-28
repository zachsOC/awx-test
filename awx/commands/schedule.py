"""Awx schedule helper module."""
from ..base import AwxBase

# TODO: Add in additional parameters that are optional for all methods.


class AwxSchedule(AwxBase):
    """Awx schedule class."""
    __resource_name__ = 'schedule'

    def __init__(self):
        """Constructor."""
        super(AwxSchedule, self).__init__()
