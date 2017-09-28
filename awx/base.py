"""Awx base module."""
from tower_cli import get_resource


class AwxBase(object):
    """Awx base class."""
    __resource_name__ = None

    @property
    def name(self):
        """Return resource name."""
        return self.__resource_name__

    @property
    def resource(self):
        """Return resource class object."""
        return get_resource(self.name)
