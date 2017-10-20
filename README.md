# AWX-TEST

AWX-test is a project that is based on using the Ansible
[tower-cli](https://github.com/ansible/tower-cli) to perform actions
within [AWX](https://github.com/ansible/awx). It provides you with a
simple Python class which uses tower-cli to run its available commands.

## Benefit

One of the main reasons for the Python class is that each of the
tower-cli commands require objects from other tower-cli commands.
For example: when creating an inventory you need to have the
organization id to associate the inventory too. You cannot pass the
name of the organization in string format. This requires you too
create an object for organization resource, get the organization object
and return the organization id to create an inventory. There was also
checks needed to see if the organization was valid, etc. This class
allows all commands (organization, host, etc) to have access to the
required commands it may need.

## Usage

Here are some examples on how to use the Python class wrapping tower-cli
library.

```python
from awx import Awx
from pprint import pprint

# create awx object
awx = Awx()

# list all organizations
print(awx.organizations.organizations)

# list all inventories
print(awx.inventory.inventories)

# create organization
awx.organization.create('minions')
```
