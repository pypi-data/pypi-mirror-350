# -*- coding: utf-8 -*-
from datetime import datetime
import re
from typing import Optional

from pip_services4_components.config import ConfigParams, IConfigurable
from pip_services4_components.context import IContext
from pip_services4_components.refer import IReferenceable, IReferences, Descriptor
from pip_services4_data.keys import IdGenerator
from pip_services4_data.query import DataPage, FilterParams, PagingParams
from pip_services4_observability.log import CompositeLogger
from pip_services4_commons.errors import BadRequestException, NotFoundException

from ..data import AccountV1
from ..data.AccountActivityTypeV1 import AccountActivityTypeV1
from ..persistence import IAccountsPersistence
from ..logic.IAccountsService import IAccountsService

# # Optional dependency
# try:
#     from client_activities_python import IActivitiesClientV1, PartyActivityV1
# except ImportError:
#     IActivitiesClientV1 = None
#     PartyActivityV1 = None


class AccountsService(IAccountsService, IConfigurable, IReferenceable):
    _persistence: IAccountsPersistence = None
    # _activities_client: Optional[IActivitiesClientV1] = None
    _logger: CompositeLogger = CompositeLogger()
    _login_as_email: bool = False

    _email_regex = re.compile(r'^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@'
                              r'((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$')

    def configure(self, config: ConfigParams):
        self._login_as_email = config.get_as_boolean_with_default('options.login_as_email', self._login_as_email)

    def set_references(self, references: IReferences):
        self._logger.set_references(references)
        self._persistence = references.get_one_required(Descriptor('aichatusers-accounts', 'persistence', '*', '*', '1.0'))
        # self._activities_client = references.get_one_optional(Descriptor('aichatactivities', 'client', '*', '*', '1.0'))

    def get_accounts(self, context: Optional[IContext], filter_params: FilterParams, paging: PagingParams) -> DataPage:
        return self._persistence.get_page_by_filter(context, filter_params, paging)

    def get_account_by_id(self, context: Optional[IContext], account_id: str) -> AccountV1:
        return self._persistence.get_one_by_id(context, account_id)

    def get_account_by_login(self, context: Optional[IContext], login: str) -> AccountV1:
        return self._persistence.get_one_by_login(context, login)

    def get_account_by_id_or_login(self, context: Optional[IContext], id_or_login: str) -> AccountV1:
        return self._persistence.get_one_by_id_or_login(context, id_or_login)

    def create_account(self, context: Optional[IContext], account: AccountV1) -> AccountV1:
        self._validate_account(context, account)

        existing = self._persistence.get_one_by_login(context, account.login)
        if existing:
            raise BadRequestException(context, 'ALREADY_EXIST', f'User account {account.login} already exists') \
                .with_details('login', account.login)

        account.id = account.id or IdGenerator.next_long()
        account.active = account.active if account.active is not None else True
        account.create_time = account.create_time or datetime.now()

        created = self._persistence.create(context, account)
        self._log_user_activity(context, created, AccountActivityTypeV1.AccountCreated)
        return created

    def update_account(self, context: Optional[IContext], account: AccountV1) -> AccountV1:
        self._validate_account(context, account)

        data = self._persistence.get_one_by_login(context, account.login)
        if data and data.id != account.id:
            raise BadRequestException(context, 'ALREADY_EXIST', f'Login {account.login} is already in use') \
                .with_details('login', account.login)

        old = self._persistence.get_one_by_id(context, account.id)
        if not old:
            raise NotFoundException(context, 'NOT_FOUND', f'Account {account.id} was not found') \
                .with_details('id', account.id)

        updated = self._persistence.update(context, account)
        self._log_user_activity(context, updated, AccountActivityTypeV1.AccountChanged)
        return updated

    def delete_account_by_id(self, context: Optional[IContext], account_id: str) -> AccountV1:
        account = self._persistence.get_one_by_id(context, account_id)
        if not account:
            return None

        account.deleted = True
        deleted = self._persistence.update(context, account)

        self._log_user_activity(context, deleted, AccountActivityTypeV1.AccountDeleted)
        return deleted

    def drop_account_by_id(self, context: Optional[IContext], account_id: str) -> AccountV1:
        account = self._persistence.delete_by_id(context, account_id)
        if account:
            self._log_user_activity(context, account, AccountActivityTypeV1.AccountDropped)
        return account

    def _validate_account(self, context: Optional[IContext], account: AccountV1):
        if not account.name:
            raise BadRequestException(context, 'NO_NAME', 'Missing account name')

        if self._login_as_email:
            if not account.login:
                raise BadRequestException(context, 'NO_EMAIL', 'Missing account email')
            if not self._email_regex.match(account.login):
                raise BadRequestException(context, 'WRONG_EMAIL', f'Invalid email: {account.login}') \
                    .with_details('login', account.login)
        else:
            if not account.login:
                raise BadRequestException(context, 'NO_LOGIN', 'Missing account login')

    def _log_user_activity(self, context: Optional[IContext], account: AccountV1, activity_type: str):
        pass
        # if self._activities_client and PartyActivityV1:
        #     try:
        #         activity = PartyActivityV1(
        #             None,
        #             activity_type,
        #             {'id': account.id, 'type': 'account', 'name': account.name}
        #         )
        #         self._activities_client.log_party_activity(context, activity)
        #     except Exception as err:
        #         self._logger.error(context, err, "Failed to log user activity")
