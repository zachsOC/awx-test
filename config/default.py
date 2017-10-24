"""Configure Ansible AWX static configuration.

This script is to be run one time only to pre configure the server for future
automated use. This will require ADMINISTRATOR access to your AWX server.
Please make sure your /etc/tower/tower_cli.cfg has the admin authentication
details before running. If they do not, you may get privilege failures.

Before running, update the organizations and users based on your needs.
"""
from awx import Awx

ORGANIZATIONS = [
    {
        'name': 'Carbon',
        'description': 'Carbon Organization'
    }
]

USERS = [
    {
        'first_name': 'Carbon',
        'last_name': 'Normal',
        'organization': 'Carbon',
        'email': 'carbon@carbon.com',
        'username': 'carbon',
        'password': 'password',
        'system_admin': False,
        'system_auditor': False,
        'organization_admin': True
    },
    {
        'first_name': 'Carbon',
        'last_name': 'Auditor',
        'organization': 'Carbon',
        'email': 'carbon-auditor@carbon.com',
        'username': 'carbon-auditor',
        'password': 'password',
        'system_admin': False,
        'system_auditor': True,
        'organization_admin': False
    }
]


def main():
    """Main function.

    Primary purpose is to configure AWX server with config information such as:
        - organizations
        - users
    """
    # create awx object
    awx = Awx()

    # create organizations
    for item in ORGANIZATIONS:
        try:
            awx.organization.create(
                name=item['name'],
                description=item['description']
            )
        except Exception:
            awx.logger.warn('Skip creating organization..')

    # create users
    for item in USERS:
        try:
            # create
            awx.user.create(
                name=item['username'],
                password=item['password'],
                email=item['email'],
                first_name=item['first_name'],
                last_name=item['last_name'],
                superuser=item['system_admin'],
                system_auditor=item['system_auditor']
            )

            # associate user to their organization
            awx.organization.associate(
                name=item['username'],
                organization=item['organization']
            )

            # associate user with admin privilege to organization
            if item['organization_admin']:
                # admin privilege
                awx.organization.associate_admin(
                    name=item['username'],
                    organization=item['organization']
                )
        except Exception:
            awx.logger.warn('Skip creating user..')


if '__main__' == __name__:
    main()
