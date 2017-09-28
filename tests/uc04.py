"""Use case 04.

This use case will demonstrate using tower-cli client library to perform the
following actions with Ansible AWX:

    1. Create an organization.
    2. Create an inventory.
    3. Create a credential
    3. Create a host.
    4. Create a project from scm - git.
    5. Create a template based on project just created.
    6. Run template.
    7. Delete template.
    8. Delete project.
    9. Delete organization (which deletes inventories and hosts associated).
"""
from time import sleep

from awx import Awx

# commonly used variables
ORGANIZATION = 'demo_organization01'
CREDENTIAL = 'Demo Credential'
INVENTORY = 'demo_inventory01'
HOST = 'localhost'
PROJECT = 'demo_project01'
JOB_TEMPLATE = 'demo_template01'

# create awx object
awx = Awx()

# create organization
awx.organization.create(
    name=ORGANIZATION,
    description='A demo organization for testing purposes.'
)

# create inventory
awx.inventory.create(
    name=INVENTORY,
    organization=ORGANIZATION,
    description='A demo inventory for testing purposes.'
)

# create a host
awx.host.create(
    name=HOST,
    inventory=INVENTORY,
    variables=dict(ansible_connection='local')
)

# create a project
awx.project.create_scm_project(
    name=PROJECT,
    description='A demo project for testing purposes.',
    organization=ORGANIZATION,
    scm_type='git',
    url='https://github.com/rywillia/awx-test'
)

sleep(15)

# create template
awx.job_template.create(
    name=JOB_TEMPLATE,
    description='A demo job template for testing purposes.',
    job_type='run',
    inventory=INVENTORY,
    project=PROJECT,
    playbook='playbooks/system-release.yml',
    credential=CREDENTIAL
)

# run template
awx.job.launch(
    name=JOB_TEMPLATE,
    reason='A demo job launch for testing purposes.'
)

# delay
sleep(30)

# delete template
awx.job_template.delete(
    name=JOB_TEMPLATE,
    project=PROJECT
)

# delete project
awx.project.delete(name=PROJECT)

# delete organization
awx.organization.delete(name=ORGANIZATION)
