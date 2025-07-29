# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from typing import Optional

from pip_services4_components.context import IContext
from pip_services4_data.query import DataPage, FilterParams, PagingParams

from ..data import AccountV1


class IAccountsService(ABC):

    @abstractmethod
    def get_accounts(self, context: Optional[IContext], filter_params: FilterParams, paging: PagingParams) -> DataPage:
        raise NotImplementedError()

    @abstractmethod
    def get_account_by_id(self, context: Optional[IContext], account_id: str) -> AccountV1:
        raise NotImplementedError()

    @abstractmethod
    def get_account_by_login(self, context: Optional[IContext], login: str) -> AccountV1:
        raise NotImplementedError()

    @abstractmethod
    def get_account_by_id_or_login(self, context: Optional[IContext], id_or_login: str) -> AccountV1:
        raise NotImplementedError()

    @abstractmethod
    def create_account(self, context: Optional[IContext], account: AccountV1) -> AccountV1:
        raise NotImplementedError()

    @abstractmethod
    def update_account(self, context: Optional[IContext], account: AccountV1) -> AccountV1:
        raise NotImplementedError()

    @abstractmethod
    def delete_account_by_id(self, context: Optional[IContext], account_id: str) -> AccountV1:
        raise NotImplementedError()

    @abstractmethod
    def drop_account_by_id(self, context: Optional[IContext], account_id: str) -> AccountV1:
        raise NotImplementedError()
