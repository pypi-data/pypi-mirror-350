# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from typing import Optional

from pip_services4_components.context import IContext
from pip_services4_data.query import DataPage, FilterParams, PagingParams

from ..data import AccountV1


class IAccountsPersistence(ABC):
    @abstractmethod
    def get_page_by_filter(self, context: Optional[IContext], filter: FilterParams, paging: PagingParams) -> DataPage:
        pass

    @abstractmethod
    def get_one_by_id(self, context: Optional[IContext], id: str) -> Optional[AccountV1]:
        pass

    @abstractmethod
    def get_one_by_login(self, context: Optional[IContext], login: str) -> Optional[AccountV1]:
        pass

    @abstractmethod
    def get_one_by_id_or_login(self, context: Optional[IContext], id_or_login: str) -> Optional[AccountV1]:
        pass

    @abstractmethod
    def create(self, context: Optional[IContext], account: AccountV1) -> AccountV1:
        pass

    @abstractmethod
    def update(self, context: Optional[IContext], account: AccountV1) -> AccountV1:
        pass

    @abstractmethod
    def delete_by_id(self, context: Optional[IContext], id: str) -> Optional[AccountV1]:
        pass
