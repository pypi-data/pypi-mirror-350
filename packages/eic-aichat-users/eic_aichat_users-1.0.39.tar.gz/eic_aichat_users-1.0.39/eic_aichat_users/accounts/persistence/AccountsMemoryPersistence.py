# -*- coding: utf-8 -*-
from datetime import datetime
from typing import Optional, Callable, Any
from pip_services4_components.context import IContext
from pip_services4_data.query import DataPage, FilterParams, PagingParams, SortParams
from pip_services4_persistence.persistence import IdentifiableMemoryPersistence
from pip_services4_commons.errors import BadRequestException

from ..data import AccountV1
from .IAccountsPersistence import IAccountsPersistence


class AccountsMemoryPersistence(IdentifiableMemoryPersistence, IAccountsPersistence):

    def __init__(self):
        super().__init__()

    def __match_string(self, value: str, search: str) -> bool:
        if value is None and search is None:
            return True
        if value is None or search is None:
            return False
        return search.lower() in value.lower()

    def __match_search(self, item: AccountV1, search: str) -> bool:
        return self.__match_string(item.name, search) or self.__match_string(item.login, search)

    def __compose_filter(self, filter: FilterParams) -> Callable[[AccountV1], bool]:
        filter = filter or FilterParams()

        search = filter.get_as_nullable_string('search')
        id = filter.get_as_nullable_string('id')
        ids = filter.get_as_object('ids')
        name = filter.get_as_nullable_string('name')
        login = filter.get_as_nullable_string('login')
        active = filter.get_as_nullable_boolean('active')
        from_create_time = filter.get_as_nullable_datetime('from_create_time')
        to_create_time = filter.get_as_nullable_datetime('to_create_time')
        deleted = filter.get_as_boolean_with_default('deleted', False)

        if isinstance(ids, str):
            ids = ids.split(',')
        if not isinstance(ids, list):
            ids = None

        def filter_func(item: AccountV1) -> bool:
            if id and item.id != id:
                return False
            if ids and item.id not in ids:
                return False
            if name and item.name != name:
                return False
            if login and item.login != login:
                return False
            if active is not None and item.active != active:
                return False
            if from_create_time and item.create_time < from_create_time:
                return False
            if to_create_time and item.create_time >= to_create_time:
                return False
            if not deleted and getattr(item, 'deleted', False):
                return False
            if search and not self.__match_search(item, search):
                return False
            return True

        return filter_func

    def get_page_by_filter(self, context: Optional[IContext], filter: FilterParams,
                           paging: PagingParams, sort: SortParams = None, select: Any = None) -> DataPage:
        return super().get_page_by_filter(context, self.__compose_filter(filter), paging)

    def get_one_by_login(self, context: Optional[IContext], login: str) -> Optional[AccountV1]:
        item = next((x for x in self._items if x.login == login), None)
        return item

    def get_one_by_id_or_login(self, context: Optional[IContext], id_or_login: str) -> Optional[AccountV1]:
        item = next((x for x in self._items if x.id == id_or_login or x.login == id_or_login), None)
        return item

    def create(self, context: Optional[IContext], item: AccountV1) -> AccountV1:
        if item is None:
            return None

        existing = next((x for x in self._items if x.login == item.login), None)
        if existing:
            raise BadRequestException(context, 'ALREADY_EXIST', f"Account {item.login} already exists")\
                .with_details('login', item.login)

        item.active = getattr(item, 'active', True)
        item.create_time = getattr(item, 'create_time', None) or datetime.now()

        return super().create(context, item)
