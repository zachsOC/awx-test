"""Awx evaluation module."""
import json

import os
from tower_cli import get_resource
from tower_cli.exceptions import Found, NotFound


# TODO: Add in additional parameters that are optional for all methods.


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

    @property
    def credential(self):
        """Return credential class instance."""
        return AwxCredential()


class AwxAdHoc(AwxBase):
    """Awx ad hoc class."""
    __resource_name__ = 'ad_hoc'

    def __init__(self):
        """Constructor."""
        super(AwxAdHoc, self).__init__()

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


class AwxConfig(AwxBase):
    __resource_name__ = 'config'

    def __init__(self):
        super(AwxConfig, self).__init__()


class AwxCredential(AwxBase):
    """Awx credential class."""
    __resource_name__ = 'credential'

    def __init__(self):
        """Constructor."""
        super(AwxCredential, self).__init__()

    @property
    def credentials(self):
        """Return list of credentials."""
        return self.resource.list()

    def create(self, name, kind, organization, **kwargs):
        """Create a credential entry.

        :param name: Credential name.
        :type name: str
        :param kind: Credential type.
        :type kind: str
        :param organization: Organization name.
        :type organization: str
        :param kwargs: key=value data for optional arguments.
        :type dict
        """
        supported_kinds = ['ssh']

        # quit if kind not supported
        if kind not in supported_kinds:
            raise Exception('Kind %s is invalid.' % kind)

        # check if organization exists
        _org = self.organization.get(organization)

        # quit if organization not found
        if not _org:
            raise Exception('Organization %s not found.' % organization)

        # call method for credential support
        getattr(self, '_create_%s_kind' % kind)(
            name,
            kind,
            _org,
            kwargs
        )

    def _create_ssh_kind(self, name, kind, organization, kwargs):
        """Create a SSH credential entry.

        :param name: Credential name.
        :type name: str
        :param kind: Credential type.
        :type kind: str
        :param organization: Organization name.
        :type organization: str
        :param kwargs: key=value data for optional arguments.
        :type dict
        """
        key = 'ssh_key_data'

        # quit if required key not defined
        if key not in kwargs:
            raise Exception('Kwargs requires %s.' % key)

        # check if ssh private key exists
        if not os.path.exists(kwargs['ssh_key_data']):
            raise Exception('SSH private key %s not located.' % key)

        # load ssh private key
        with open(kwargs[key], 'r') as fh:
            key_content = fh.read()

        # create credential entry
        self.resource.create(
            name=name,
            kind=kind,
            organization=organization['id'],
            ssh_key_data=key_content
        )

    def delete(self, name, kind):
        """Delete a credential entry."""
        self.resource.delete(name=name, kind=kind)

    def get(self, name):
        """Get credential.

        :param name: Credential name.
        :type name: str
        :return: Credential object.
        :type dict
        """
        try:
            return self.resource.get(name=name)
        except NotFound as ex:
            raise Exception(ex.message)


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

    def create(self, name, inventory, variables=None):
        """Create a host."""
        # check if inventory exists
        try:
            _inv = self.inventory.get(inventory)
        except Exception:
            raise Exception('Inventory %s not found.' % inventory)

        self.resource.create(
            name=name,
            inventory=_inv['id'],
            variables=json.dumps(variables)
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

    def create(self, name, description=None):
        """Create an organization.

        :param name: Organization name.
        :type name: str
        :param description: Organization description.
        :type description: str
        """
        try:
            self.resource.create(
                name=name,
                description=description,
                fail_on_found=True
            )
        except Found as ex:
            raise Exception(ex.message)

    def delete(self, name):
        """Delete an organization.

        :param name: Organization name.
        :type name: str
        """
        self.resource.delete(name=name)

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
    """Awx user class."""
    __resource_name__ = 'user'

    def __init__(self):
        """Constructor."""
        super(AwxUser, self).__init__()


    @property
    def users(self):
        """Return list of users."""
        return self.resource.list()

    def create(self, name, password, email, first_name, last_name,
               superuser=False, system_auditor=False):
        """Create a user.

        :param name: Username.
        :type name: str
        :param password: Password.
        :type password: str
        :param email: Email address.
        :type email: str
        :param first_name: First name.
        :type first_name: str
        :param last_name: Last name.
        :type last_name: str
        :param superuser: Superuser field.
        :type superuser: bool
        :param system_auditor: System auditor field.
        :type system_auditor: bool
        """
        try:
            self.resource.create(
                username=name,
                password=password,
                email=email,
                first_name=first_name,
                last_name=last_name,
                is_superuser=superuser,
                is_system_auditor=system_auditor,
                fail_on_found=True
            )
        except Found as ex:
            raise Exception(ex.message)

    def delete(self, name):
        """Delete a user.

        :param name: Username.
        :type name: str
        """
        self.resource.delete(username=name)

    def get(self, name):
        """Get a user.

        :param name: Username.
        :type name: str
        """
        try:
            return self.resource.get(username=name)
        except NotFound as ex:
            raise Exception(ex.message)


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


class Awx(object):
    """Awx class."""

    def __init__(self):
        """Constructor."""
        self._ad_hoc = AwxAdHoc()
        self._config = AwxConfig()
        self._credential = AwxCredential()
        self._group = AwxGroup()
        self._host = AwxHost()
        self._inventory = AwxInventory()
        self._inventory_script = AwxInventoryScript()
        self._job = AwxJob()
        self._job_template = AwxJobTemplate()
        self._label = AwxLabel()
        self._node = AwxNode()
        self._notification_template = AwxNotificationTemplate()
        self._organization = AwxOrganization()
        self._permission = AwxPermission()
        self._project = AwxProject()
        self._role = AwxRole()
        self._schedule = AwxSchedule()
        self._setting = AwxSetting()
        self._team = AwxTeam()
        self._user = AwxUser()
        self._version = AwxVersion()
        self._workflow = AwxWorkflow()
        self._workflow_job = AwxWorkflowJob()

    @property
    def ad_hoc(self):
        """Return ad hoc instance."""
        return self._ad_hoc

    @property
    def config(self):
        """Return config instance."""
        return self._config

    @property
    def credential(self):
        """Return credential instance."""
        return self._credential

    @property
    def group(self):
        """Return group instance."""
        return self._group

    @property
    def host(self):
        """Return host instance."""
        return self._host

    @property
    def inventory(self):
        """Return inventory instance."""
        return self._inventory

    @property
    def inventory_script(self):
        """Return inventory script instance."""
        return self._inventory_script

    @property
    def job(self):
        """Return job instance."""
        return self._job

    @property
    def job_template(self):
        """Return job template instance."""
        return self._job_template

    @property
    def label(self):
        """Return label instance."""
        return self._label

    @property
    def node(self):
        """Return node instance."""
        return self._node

    @property
    def notification_template(self):
        """Return notification template instance."""
        return self._notification_template

    @property
    def organization(self):
        """Return organization instance."""
        return self._organization

    @property
    def permission(self):
        """Return permission instance."""
        return self._permission

    @property
    def project(self):
        """Return project instance."""
        return self._project

    @property
    def role(self):
        """Return role instance."""
        return self._role

    @property
    def schedule(self):
        """Return schedule instance."""
        return self._schedule

    @property
    def setting(self):
        """Return setting instance."""
        return self._setting

    @property
    def team(self):
        """Return team instance."""
        return self._team

    @property
    def user(self):
        """Return user instance."""
        return self._user

    @property
    def version(self):
        """Return version instance."""
        return self._version

    @property
    def workflow(self):
        """Return workflow instance."""
        return self._workflow

    @property
    def workflow_job(self):
        """Return workflow job instance."""
        return self._workflow_job
