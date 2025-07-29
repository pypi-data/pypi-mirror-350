# -*- coding: utf-8 -*-
from pip_services4_components.config import ConfigParams
from pip_services4_components.refer import References, Descriptor
from pip_services4_data.query import PagingParams, FilterParams

from eic_aichat_users.accounts.data.AccountV1 import AccountV1
from eic_aichat_users.accounts.logic.AccountsService import AccountsService
from eic_aichat_users.accounts.persistence.AccountsMemoryPersistence import AccountsMemoryPersistence


ACCOUNT1 = AccountV1('1', 'user1@conceptual.vision', 'Test User 1')
ACCOUNT2 = AccountV1('2', 'user2@conceptual.vision', 'Test User 2')


class TestAccountsService:
    persistence: AccountsMemoryPersistence
    service: AccountsService

    def setup_method(self):
        self.persistence = AccountsMemoryPersistence()
        self.persistence.configure(ConfigParams())

        self.service = AccountsService()
        self.service.configure(ConfigParams.from_tuples(
            'options.login_as_email', True
        ))

        references = References.from_tuples(
            Descriptor('aichatusers-accounts', 'persistence', 'memory', 'default', '1.0'), self.persistence,
            Descriptor('aichatusers-accounts', 'service', 'default', 'default', '1.0'), self.service
        )

        self.service.set_references(references)

        self.persistence.open(None)
        self.persistence.clear(None)

    def teardown_method(self):
        self.persistence.close(None)

    def test_create_new_account(self):
        account = self.service.create_account(None, ACCOUNT1)
        assert account is not None
        assert account.name == ACCOUNT1.name
        assert account.login == ACCOUNT1.login

    def test_fail_to_create_duplicate_account(self):
        # First creation
        account = self.service.create_account(None, ACCOUNT1)
        assert account is not None

        # Second creation with same login should fail
        error = None
        try:
            self.service.create_account(None, ACCOUNT1)
        except Exception as e:
            error = e

        assert error is not None

    def test_get_accounts(self):
        account1 = self.service.create_account(None, ACCOUNT1)
        account2 = self.service.create_account(None, ACCOUNT2)

        # Get account by ID
        result = self.service.get_account_by_id(None, account1.id)
        assert result is not None
        assert result.id == account1.id

        # Get account by login
        result = self.service.get_account_by_id_or_login(None, account2.login)
        assert result is not None
        assert result.id == account2.id

        # Get all accounts
        page = self.service.get_accounts(None, FilterParams(), PagingParams())
        assert page is not None
        assert len(page.data) == 2

    def test_update_account(self):
        account = self.service.create_account(None, ACCOUNT1)
        account.name = 'Updated Name'
        updated = self.service.update_account(None, account)

        assert updated is not None
        assert updated.name == 'Updated Name'

    def test_change_account_email(self):
        account = self.service.create_account(None, ACCOUNT1)
        account.login = 'new@email.com'
        account.name = 'New Name'

        updated = self.service.update_account(None, account)
        assert updated is not None
        assert updated.login == 'new@email.com'
        assert updated.name == 'New Name'
