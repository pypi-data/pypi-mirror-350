# -*- coding: utf-8 -*-
from pip_services4_components.config import ConfigParams
from pip_services4_components.refer import References, Descriptor
from pip_services4_data.query import FilterParams

from eic_aichat_users.roles.logic.RolesService import RolesService
from eic_aichat_users.roles.persistence.RolesMemoryPersistence import RolesMemoryPersistence

ROLES = ['Role 1', 'Role 2', 'Role 3']


class TestRolesService:
    persistence: RolesMemoryPersistence
    service: RolesService

    def setup_method(self):
        self.persistence = RolesMemoryPersistence()
        self.persistence.configure(ConfigParams())

        self.service = RolesService()
        self.service.configure(ConfigParams())

        references = References.from_tuples(
            Descriptor('aichatusers-roles', 'persistence', 'memory', 'default', '1.0'), self.persistence,
            Descriptor('aichatusers-roles', 'service', 'default', 'default', '1.0'), self.service
        )

        self.service.set_references(references)

        self.persistence.open(None)
        self.persistence.clear(None)

    def teardown_method(self):
        self.persistence.close(None)

    def test_get_and_set_roles(self):
        roles = self.service.set_roles(None, '1', ROLES)
        assert roles is not None
        assert len(roles) == 3

        roles = self.service.get_roles_by_id(None, '1')
        assert roles is not None
        assert len(roles) == 3

    def test_grant_and_revoke_roles(self):
        roles = self.service.grant_roles(None, '1', ['Role 1'])
        assert roles == ['Role 1']

        roles = self.service.grant_roles(None, '1', ['Role 1', 'Role 2', 'Role 3'])
        assert sorted(roles) == sorted(ROLES)

        roles = self.service.revoke_roles(None, '1', ['Role 1'])
        assert sorted(roles) == ['Role 2', 'Role 3']

        roles = self.service.revoke_roles(None, '1', ['Role 1', 'Role 2'])
        assert roles == ['Role 3']

    def test_authorize_roles(self):
        self.service.grant_roles(None, '1', ['Role 1', 'Role 2'])

        result = self.service.authorize(None, '1', ['Role 1'])
        assert result is True

        result = self.service.authorize(None, '1', ['Role 2', 'Role 3'])
        assert result is False
