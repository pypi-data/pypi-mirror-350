# -*- coding: utf-8 -*-
from pip_services4_data.query import FilterParams, PagingParams
from eic_aichat_users.accounts.data.AccountV1 import AccountV1
from eic_aichat_users.accounts.persistence.IAccountsPersistence import IAccountsPersistence


ACCOUNT1 = AccountV1('1', 'user1@conceptual.vision', 'Test User 1')
ACCOUNT2 = AccountV1('2', 'user2@conceptual.vision', 'Test User 2')
ACCOUNT3 = AccountV1('3', 'user3@conceptual.vision', 'Test User 3')


class AccountsPersistenceFixture:
    _persistence: IAccountsPersistence

    def __init__(self, persistence: IAccountsPersistence):
        assert persistence is not None
        self._persistence = persistence

    def __create_accounts(self):
        # Create the first account
        account = self._persistence.create(None, ACCOUNT1)
        assert ACCOUNT1.id == account.id
        assert ACCOUNT1.login == account.login
        assert ACCOUNT1.name == account.name
        assert account.active is True

        # Create the second account
        account = self._persistence.create(None, ACCOUNT2)
        assert ACCOUNT2.id == account.id
        assert ACCOUNT2.login == account.login
        assert ACCOUNT2.name == account.name
        assert account.active is True

        # Create the third account
        account = self._persistence.create(None, ACCOUNT3)
        assert ACCOUNT3.id == account.id
        assert ACCOUNT3.login == account.login
        assert ACCOUNT3.name == account.name
        assert account.active is True

    def test_crud_operations(self):
        # Create accounts
        self.__create_accounts()

        # Get all accounts
        page = self._persistence.get_page_by_filter(None, FilterParams(), PagingParams())
        assert page is not None
        assert len(page.data) == 3

        account1 = page.data[0]

        # Update the account
        account1.name = 'Updated User 1'
        account = self._persistence.update(None, account1)

        assert account.id == account1.id
        assert account.name == 'Updated User 1'
        assert account.login == account1.login

        # Delete the account
        self._persistence.delete_by_id(None, ACCOUNT1.id)

        # Try to get deleted account
        deleted = self._persistence.get_one_by_id(None, ACCOUNT1.id)
        assert deleted is None

    def test_get_with_filter(self):
        # Create accounts
        self.__create_accounts()

        # Get accounts by search
        page = self._persistence.get_page_by_filter(
            None,
            FilterParams.from_tuples('active', True, 'search', 'user'),
            PagingParams()
        )
        assert page is not None
        assert len(page.data) == 3

        # Get account by login
        account = self._persistence.get_one_by_login(None, ACCOUNT2.login)
        assert account is not None
        assert account.id == ACCOUNT2.id

        # Get account by id or login
        account = self._persistence.get_one_by_id_or_login(None, ACCOUNT3.login)
        assert account is not None
        assert account.id == ACCOUNT3.id
