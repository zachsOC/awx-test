"""Awx notification template helper module."""

from ..base import AwxBase

# TODO: Add in additional parameters that are optional for all methods.


class AwxNotificationTemplate(AwxBase):
    """Awx notification template class."""
    __resource_name__ = 'notification_template'

    def __init__(self):
        """Constructor."""
        super(AwxNotificationTemplate, self).__init__()
