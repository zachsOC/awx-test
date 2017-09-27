"""Use case 01.

This use case will demonstrate using tower-cli client library to perform
the following actions with Ansible AWX:

    1. Create a new organization
    2. Create a new inventory
    3. Create a new host (adding to previously created inventory)
    4. Run a ad hoc ping command on host
    5. Delete host
    6. Delete inventory
    7. Delete organization
"""
from awx.awx import AwxAdHoc
from awx.awx import AwxCredential
from awx.awx import AwxHost
from awx.awx import AwxInventory
from awx.awx import AwxOrganization
from time import sleep

# global variables
CREDENTIAL = 'Demo Credential'
HOST = 'localhost'
INVENTORY = 'uc01'
ORGANIZATION = 'uc01'

# create awx objects
awx_adhoc = AwxAdHoc()
awx_credential = AwxCredential()
awx_host = AwxHost()
awx_inventory = AwxInventory()
awx_organization = AwxOrganization()

# create organization
awx_organization.create(ORGANIZATION)

# create inventory
awx_inventory.create(INVENTORY, ORGANIZATION)

# create host
awx_host.create(
    HOST,
    INVENTORY,
    dict(ansible_connection='local')
)

# run ad hoc command (ping host)
awx_adhoc.launch(
    'run',
    'ping',
    INVENTORY,
    CREDENTIAL
)

sleep(20)

# delete host
awx_host.delete(HOST, INVENTORY)

# delete inventory
awx_inventory.delete(INVENTORY)

# delete organization
awx_organization.delete(ORGANIZATION)
