# -*- coding: utf-8 -*-
from eic_aichat_users.roles.persistence.RolesMemoryPersistence import RolesMemoryPersistence
from test.roles.persistence.RolesPersistenceFixture import RolesPersistenceFixture


class TestRolesMemoryPersistence:
    persistence: RolesMemoryPersistence
    fixture: RolesPersistenceFixture

    def setup_method(self):
        self.persistence = RolesMemoryPersistence()
        self.fixture = RolesPersistenceFixture(self.persistence)

        self.persistence.open(None)
        self.persistence.clear(None)

    def teardown_method(self):
        self.persistence.close(None)

    def test_get_and_set_roles(self):
        self.fixture.test_get_and_set_roles()
