"""Use case 03.

This use case will demonstrate using tower-cli client library to perform
the following actions with Ansible AWX:

    1. Create a new scm project.
    2. List projects.
    3. Delete scm project.
    4. Create new manual project.
    5. List projects.
    6. Delete manual project.
"""
from pprint import pprint
from time import sleep

from awx.awx import Awx


def list_projects():
    for project in awx.project.projects['results']:
        pprint(dict(project), indent=4)

# create awx object
awx = Awx()

# create scm project
awx.project.create_scm_project(
    'demo01',
    'Project demonstrating SCM by git',
    'Default',
    'git',
    'http://github.com/rywillia/awx-test'
)

# list projects
list_projects()

# delay
sleep(5)

# delete scm project
awx.project.delete('demo01')

# create manual project
awx.project.create_manual_project(
    'demo02',
    'Project demonstrating SCM by manual',
    'Default'
)

# list projects
list_projects()

# delay
sleep(5)

# delete manual project
awx.project.delete('demo02')
