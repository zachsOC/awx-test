"""Awx ad hoc helper module."""
from .credential import AwxCredential
from .inventory import AwxInventory
from ..base import AwxBase


# TODO: Add in additional parameters that are optional for all methods.


class AwxAdHoc(AwxBase):
    """Awx ad hoc class."""
    __resource_name__ = 'ad_hoc'

    def __init__(self):
        """Constructor."""
        super(AwxAdHoc, self).__init__()
        self._credential = AwxCredential()
        self._inventory = AwxInventory()

    @property
    def credential(self):
        """Return credential instance."""
        return self._credential

    @property
    def inventory(self):
        """Return inventory instance."""
        return self._inventory

    @property
    def ad_hocs(self):
        """Return list of ad hocs."""
        return self.resource.list()

    def launch(self, job_type, module, inventory, credential):
        """Launch a ad hoc command.

        :param job_type: Job type field.
        :type job_type: str
        :param module: Module name.
        :type module: str
        :param inventory: Inventory field.
        :type inventory: str
        :param credential: Credential field.
        :type credential: str
        :return: Launch data
        :rtype: dict
        """
        # get credential object
        _credential = self.credential.get(credential)

        # get inventory object
        _inventory = self.inventory.get(inventory)

        return self.resource.launch(
            job_type=job_type,
            module_name=module,
            inventory=_inventory['id'],
            credential=_credential['id']
        )
