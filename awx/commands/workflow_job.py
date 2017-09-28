"""Awx workflow job helper module."""
from ..base import AwxBase

# TODO: Add in additional parameters that are optional for all methods.


class AwxWorkflowJob(AwxBase):
    """Awx workflow job class."""
    __resource_name__ = 'workflow_job'

    def __init__(self):
        """Constructor."""
        super(AwxWorkflowJob, self).__init__()
