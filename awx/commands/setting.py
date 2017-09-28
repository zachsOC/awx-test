"""Awx setting helper module."""
from ..base import AwxBase

# TODO: Add in additional parameters that are optional for all methods.


class AwxSetting(AwxBase):
    """Awx setting class."""
    __resource_name__ = 'setting'

    def __init__(self):
        """Constructor."""
        super(AwxSetting, self).__init__()
