"""Awx evaluation module."""
import json

import os
from tower_cli import get_resource
from tower_cli.conf import settings
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
        self._organization = AwxOrganization()

    @property
    def organization(self):
        """Return organization instance."""
        return self._organization

    @property
    def credentials(self):
        """Return list of credentials."""
        return self.resource.list()

    def create_ssh_credential(self, name, organization, ssh_key_file):
        """Create a SSH credential entry.

        :param name: Credential name.
        :type name: str
        :param organization: Organization name.
        :type organization: str
        :param ssh_key_file: SSH private key file path.
        :type ssh_key_file: str
        """
        # quit if ssh private key file path does not exist
        if not os.path.exists(ssh_key_file):
            raise Exception('SSH private key %s not found.' % ssh_key_file)

        # check if organization exists
        _org = self.organization.get(organization)

        # quit if organization not found
        if not _org:
            raise Exception('Organization %s not found.' % organization)

        # load ssh private key
        with open(ssh_key_file, 'r') as fh:
            key_content = fh.read()

        # create credential entry
        self.resource.create(
            name=name,
            kind='ssh',
            organization=_org['id'],
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
        self._inventory = AwxInventory()

    @property
    def inventory(self):
        """Return inventory instance."""
        return self._inventory

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
        self._organization = AwxOrganization()

    @property
    def organization(self):
        """Return organization instance."""
        return self._organization

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
        self._inventory = AwxInventory()
        self._credential = AwxCredential()
        self._project = AwxProject()

    @property
    def project(self):
        """Return project instance."""
        return self._project

    @property
    def credential(self):
        """Return credential instance."""
        return self._credential

    @property
    def inventory(self):
        """Return inventory instance."""
        return self._inventory

    @property
    def job_templates(self):
        """Return a list of job templates."""
        return self.resource.list()

    def create(self, name, description, job_type, inventory, project, playbook,
               credential):
        """Create a job template.

        :param name: Template name.
        :type name: str
        :param description: Template description.
        :type description: str
        :param job_type: Job type.
        :type job_type: str
        :param inventory: Inventory name.
        :type inventory: str
        :param project: Project name.
        :type project: str
        :param playbook: Playbook name.
        :type playbook: str
        :param credential: Credential name.
        :type credential: str
        """
        # get credential object
        _credential = self.credential.get(credential)

        # get inventory object
        _inventory = self.inventory.get(inventory)

        # get project object
        _project = self.project.get(project)

        try:
            self.resource.create(
                name=name,
                description=description,
                job_type=job_type,
                inventory=_inventory['id'],
                project=_project['id'],
                playbook=playbook,
                credential=_credential['id']
            )
        except Found as ex:
            raise Exception(ex.message)

    def delete(self, name, project):
        """Delete a job template.

        :param name: Template name.
        :type name: str
        :param project: Project name.
        :type project: str
        """
        # get project object
        _project = self.project.get(project)

        # delete job template
        self.resource.delete(name=name, project=_project['id'])


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
    """Awx project class."""
    __resource_name__ = 'project'

    def __init__(self):
        """Constructor."""
        super(AwxProject, self).__init__()
        self._scm_types = ['manual', 'git', 'hg', 'svn']

        self._organization = AwxOrganization()

    @property
    def organization(self):
        """Return organization instance."""
        return self._organization

    @property
    def scm_types(self):
        """Return a list of scm types."""
        return self._scm_types

    @property
    def projects(self):
        """Return a list of projects."""
        return self.resource.list()

    def get(self, name):
        """Get project.

        :param name: Project name.
        :type name: str
        :return: Project object.
        :rtype: dict
        """
        try:
            return self.resource.get(name=name)
        except NotFound as ex:
            raise Exception(ex.message)

    def create_scm_project(self, name, description, organization, scm_type,
                           url, branch='master', credential=None, clean=False,
                           delete_on_update=False, update_on_launch=False,
                           update_cache_timeout=0):
        """Create project based on scm source details.

        :param name: Project name.
        :type name: str
        :param description: Project description.
        :type description: str
        :param organization: Organization name.
        :type organization: str
        :param scm_type: SCM type.
        :type scm_type: str
        :param url: SCM url.
        :type url: str
        :param branch: SCM branch name.
        :type branch: str
        :param credential: SCM credential.
        :type credential: str
        :param clean: Remove local modifications before updating.
        :type clean: bool
        :param delete_on_update: Delete local repo before updating.
        :type delete_on_update: bool
        :param update_on_launch: Update local repo on each run.
        :type update_on_launch: bool
        :param update_cache_timeout: Update local repo timeout.
        :type update_cache_timeout: int
        """
        # check if organization exists
        _org = self.organization.get(organization)

        # quit if organization not found
        if not _org:
            raise Exception('Organization %s not found.' % organization)

        try:
            self.resource.create(
                name=name,
                description=description,
                organization=_org['id'],
                scm_type=scm_type,
                scm_url=url,
                scm_branch=branch,
                scm_credential=credential,
                scm_clean=clean,
                scm_delete_on_update=delete_on_update,
                scm_update_on_launch=update_on_launch,
                scm_update_cache_timeout=update_cache_timeout,
                fail_on_found=True
            )
        except Found as ex:
            raise Exception(ex.message)

    def create_manual_project(self, name, description, organization):
        """Create project based on manual source.

        :param name: Project name.
        :type name: str
        :param description: Project description.
        :type description: str
        :param organization: Organization name.
        :type organization: str
        """
        # check if organization exists
        _org = self.organization.get(organization)

        # quit if organization not found
        if not _org:
            raise Exception('Organization %s not found.' % organization)

        try:
            self.resource.create(
                name=name,
                description=description,
                organization=_org['id'],
                scm_type='',
                fail_on_found=True
            )
        except Found as ex:
            raise Exception(ex.message)


    def delete(self, name):
        """Delete a project.

        :param name: Project name.
        :type name: str
        """
        self.resource.delete(name=name)


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

    def __init__(self, host=None, username=None, password=None):
        """Constructor.

        :param host: Ansible AWX host URL.
        :type host: str
        :param username: AWX username.
        :type username: str
        :param password: AWX password.
        :type password: str
        """
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

        # set runtime parameters, this will override ones defined by file
        self.runtime_settings('host', host)
        self.runtime_settings('username', username)
        self.runtime_settings('password', password)
        self.runtime_settings('verify_ssl', 'False')

    @staticmethod
    def runtime_settings(key, value):
        """Set run time settings.

        :param key: Key name.
        :type key: str
        :param value: Key value.
        :type value: str
        """
        if value:
            settings.set_or_reset_runtime_param(key, value)

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
