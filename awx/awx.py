"""Awx evaluation module."""
from tower_cli import get_resource
from tower_cli.exceptions import Found, NotFound


class AwxBase(object):
    __resource_name__ = None

    @property
    def name(self):
        """Return resource name."""
        return self.__resource_name__

    @property
    def resource(self):
        """Return resource class object."""
        return get_resource(self.name)

    @property
    def organization(self):
        """Return organization class instance."""
        return AwxOrganization()

    @property
    def inventory(self):
        """Return inventory class instance."""
        return AwxInventory()


class AwxAdHoc(AwxBase):
    __resource_name__ = 'ad_hoc'

    def __init__(self):
        super(AwxAdHoc, self).__init__()


class AwxConfig(AwxBase):
    __resource_name__ = 'config'

    def __init__(self):
        super(AwxConfig, self).__init__()


class AwxCredential(AwxBase):
    __resource_name__ = 'credential'

    def __init__(self):
        super(AwxCredential, self).__init__()


class AwxGroup(AwxBase):
    __resource_name__ = 'group'

    def __init__(self):
        super(AwxGroup, self).__init__()


class AwxHost(AwxBase):
    """Awx host class."""
    __resource_name__ = 'host'

    def __init__(self):
        """Constructor."""
        super(AwxHost, self).__init__()

    @property
    def hosts(self):
        """Return list of hosts."""
        return self.resource.list()

    def create(self, name, inventory):
        """Create a host."""
        # check if inventory exists
        try:
            _inv = self.inventory.get(inventory)
        except Exception:
            raise Exception('Inventory %s not found.' % inventory)

        self.resource.create(
            name=name,
            inventory=_inv['id']
        )

    def delete(self, name, inventory):
        """Delete a host."""
        # check if inventory exists
        try:
            _inv = self.inventory.get(inventory)
        except Exception:
            raise Exception('Inventory %s not found.' % inventory)

        self.resource.delete(
            name=name,
            inventory=_inv['id']
        )


class AwxInventory(AwxBase):
    """Awx inventory class."""
    __resource_name__ = 'inventory'

    def __init__(self):
        """Constructor."""
        super(AwxInventory, self).__init__()

    @property
    def inventories(self):
        """Return list of inventories."""
        return self.resource.list()

    def create(self, name, organization, description=None, variables=None):
        """Create an inventory file.

        :param name: Filename.
        :type name: str
        :param organization: Organization name.
        :type organization: str
        :param description: Inventory description.
        :type description: str
        :param variables: Inventory variables.
        :type variables: dict
        """
        # check if organization exists
        _org = self.organization.get(organization)

        # quit if organization not found
        if not _org:
            raise Exception('Organization %s not found.' % organization)

        try:
            self.resource.create(
                name=name,
                organization=_org['id'],
                description=description,
                variables=variables,
                fail_on_found=True
            )
        except Found as ex:
            raise Exception(ex.message)

    def delete(self, name):
        """Delete an inventory.

        :param name: Filename.
        :type name: str
        """
        self.resource.delete(name=name)

    def get(self, name):
        """Get inventory.

        :param name: Inventory name.
        :type name: str
        :return: Inventory object.
        :rtype: dict
        """
        try:
            return self.resource.get(name=name)
        except NotFound as ex:
            raise Exception(ex.message)


class AwxInventoryScript(AwxBase):
    __resource_name__ = 'inventory_script'

    def __init__(self):
        super(AwxInventoryScript, self).__init__()


class AwxJob(AwxBase):
    __resource_name__ = 'job'

    def __init__(self):
        super(AwxJob, self).__init__()


class AwxJobTemplate(AwxBase):
    __resource_name__ = 'job_template'

    def __init__(self):
        super(AwxJobTemplate, self).__init__()


class AwxLabel(AwxBase):
    __resource_name__ = 'label'

    def __init__(self):
        super(AwxLabel, self).__init__()


class AwxNode(AwxBase):
    __resource_name__ = 'node'

    def __init__(self):
        super(AwxNode, self).__init__()


class AwxNotificationTemplate(AwxBase):
    __resource_name__ = 'notification_template'

    def __init__(self):
        super(AwxNotificationTemplate, self).__init__()


class AwxOrganization(AwxBase):
    """Awx organization class."""
    __resource_name__ = 'organization'

    def __init__(self):
        """Constructor."""
        super(AwxOrganization, self).__init__()

    @property
    def organizations(self):
        """Return list of organizations."""
        return self.resource.list()

    def get(self, name):
        """Get organization.

        :param name: Organization name.
        :type name: str
        :return: Organization object.
        :rtype: dict
        """
        for item in self.organizations['results']:
            if item['name'] == name:
                return item
        return {}


class AwxPermission(AwxBase):
    __resource_name__ = 'permission'

    def __init__(self):
        super(AwxPermission, self).__init__()


class AwxProject(AwxBase):
    __resource_name__ = 'project'

    def __init__(self):
        super(AwxProject, self).__init__()


class AwxRole(AwxBase):
    __resource_name__ = 'role'

    def __init__(self):
        super(AwxRole, self).__init__()


class AwxSchedule(AwxBase):
    __resource_name__ = 'schedule'

    def __init__(self):
        super(AwxSchedule, self).__init__()


class AwxSetting(AwxBase):
    __resource_name__ = 'setting'

    def __init__(self):
        super(AwxSetting, self).__init__()


class AwxTeam(AwxBase):
    __resource_name__ = 'team'

    def __init__(self):
        super(AwxTeam, self).__init__()


class AwxUser(AwxBase):
    __resource_name__ = 'user'

    def __init__(self):
        super(AwxUser, self).__init__()


class AwxVersion(AwxBase):
    __resource_name__ = 'version'

    def __init__(self):
        super(AwxVersion, self).__init__()


class AwxWorkflow(AwxBase):
    __resource_name__ = 'workflow'

    def __init__(self):
        super(AwxWorkflow, self).__init__()


class AwxWorkflowJob(AwxBase):
    __resource_name__ = 'workflow_job'

    def __init__(self):
        super(AwxWorkflowJob, self).__init__()
