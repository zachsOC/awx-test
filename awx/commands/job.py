"""Awx job helper module."""
from .job_template import AwxJobTemplate
from ..base import AwxBase

# TODO: Add in additional parameters that are optional for all methods.


class AwxJob(AwxBase):
    """Awx job class."""
    __resource_name__ = 'job'

    def __init__(self):
        """Constructor."""
        super(AwxJob, self).__init__()
        self._job_template = AwxJobTemplate()

    @property
    def job_template(self):
        """Return job template instance."""
        return self._job_template

    @property
    def jobs(self):
        """Return a list of jobs."""
        return self.resource.list()

    def launch(self, name, reason):
        """Launch a new job from a job template.

        :param name: Template name.
        :type name: str
        :param reason: Reason for template launch.
        :type reason: str
        """
        # get job template object
        _job_template = self.job_template.get(name)

        self.resource.launch(
            job_template=_job_template['id'],
            job_explanation=reason
        )
