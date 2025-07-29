# -*- coding: utf-8 -*-
from eic_aichat_users.accounts.persistence.AccountsMemoryPersistence import AccountsMemoryPersistence
from test.accounts.persistence.AccountsPersistenceFixture import AccountsPersistenceFixture


class TestAccountsMemoryPersistence:
    persistence: AccountsMemoryPersistence
    fixture: AccountsPersistenceFixture

    def setup_method(self):
        self.persistence = AccountsMemoryPersistence()
        self.fixture = AccountsPersistenceFixture(self.persistence)

        self.persistence.open(None)
        self.persistence.clear(None)

    def teardown_method(self):
        self.persistence.close(None)

    def test_crud_operations(self):
        self.fixture.test_crud_operations()

    def test_get_with_filter(self):
        self.fixture.test_get_with_filter()
