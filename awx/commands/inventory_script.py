"""Awx inventory script helper module."""
from ..base import AwxBase

# TODO: Add in additional parameters that are optional for all methods.


class AwxInventoryScript(AwxBase):
    """Awx inventory script class."""
    __resource_name__ = 'inventory_script'

    def __init__(self):
        """Constructor."""
        super(AwxInventoryScript, self).__init__()
