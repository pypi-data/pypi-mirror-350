# -*- coding: utf-8 -*-
from eic_aichat_users.passwords.persistence.PasswordsMemoryPersistence import PasswordsMemoryPersistence
from test.passwords.persistence.PasswordsPersistenceFixture import PasswordsPersistenceFixture


class TestPasswordsMemoryPersistence:
    persistence: PasswordsMemoryPersistence
    fixture: PasswordsPersistenceFixture

    def setup_method(self):
        self.persistence = PasswordsMemoryPersistence()
        self.fixture = PasswordsPersistenceFixture(self.persistence)

        self.persistence.open(None)
        self.persistence.clear(None)

    def teardown_method(self):
        self.persistence.close(None)

    def test_crud_operations(self):
        self.fixture.test_crud_operations()
