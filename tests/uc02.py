"""Use case 02.

This use case will demonstrate using tower-cli client library to perform
the following actions with Ansible AWX:

    1. Create a user
    2. Delete a user
"""
from pprint import pprint

from awx.awx import Awx

# create awx objects
awx = Awx()

# create user
awx.user.create(
    'user01',
    'password',
    'user01@test.com',
    'User01',
    'User01'
)

# list users
for user in awx.user.users['results']:
    pprint(dict(user), indent=4)

# delete user
awx.user.delete('user01')
