# -*- coding: utf-8 -*-
from datetime import datetime
from typing import Optional, Any

from pip_services4_components.context import IContext
from pip_services4_data.query import DataPage, FilterParams, PagingParams
from pip_services4_mongodb.persistence import IdentifiableMongoDbPersistence

from ..data import AccountV1
from .IAccountsPersistence import IAccountsPersistence


class AccountsMongoDbPersistence(IdentifiableMongoDbPersistence, IAccountsPersistence):

    def __init__(self):
        super().__init__('accounts')
        self._max_page_size = 1000

        # Ensure unique index on login
        self._ensure_index({'login': 1}, {'unique': True})

    def __compose_filter(self, filter_params: FilterParams) -> Any:
        filter_params = filter_params or FilterParams()
        criteria = []

        search = filter_params.get_as_nullable_string('search')
        if search:
            search_regex = {'$regex': search, '$options': 'i'}
            criteria.append({'$or': [{'login': search_regex}, {'name': search_regex}]})

        id = filter_params.get_as_nullable_string('id')
        if id:
            criteria.append({'_id': id})

        ids = filter_params.get_as_object('ids')
        if isinstance(ids, str):
            ids = ids.split(',')
        if isinstance(ids, list):
            criteria.append({'_id': {'$in': ids}})

        name = filter_params.get_as_nullable_string('name')
        if name:
            criteria.append({'name': name})

        login = filter_params.get_as_nullable_string('login')
        if login:
            criteria.append({'login': login})

        active = filter_params.get_as_nullable_boolean('active')
        if active is not None:
            criteria.append({'active': active})

        from_create_time = filter_params.get_as_nullable_datetime('from_create_time')
        if from_create_time:
            criteria.append({'create_time': {'$gte': from_create_time}})

        to_create_time = filter_params.get_as_nullable_datetime('to_create_time')
        if to_create_time:
            criteria.append({'create_time': {'$lt': to_create_time}})

        deleted = filter_params.get_as_boolean_with_default('deleted', False)
        if not deleted:
            criteria.append({'$or': [{'deleted': False}, {'deleted': {'$exists': False}}]})

        return {'$and': criteria} if criteria else {}

    def get_page_by_filter(self, context: Optional[IContext], filter_params: FilterParams,
                           paging: PagingParams, sort: Any = None, select: Any = None) -> DataPage:
        sort = sort or '-create_time'
        select = select or {'custom_dat': 0}
        return super().get_page_by_filter(context, self.__compose_filter(filter_params), paging, sort, select)

    def get_one_by_login(self, context: Optional[IContext], login: str) -> Optional[AccountV1]:
        criteria = {'login': login}
        item = self._collection.find_one(criteria)

        self._logger.trace(context, "Retrieved from %s with login = %s", self._collection.name, login)
        item = self._convert_to_public(item)

        return item

    def get_one_by_id_or_login(self, context: Optional[IContext], id_or_login: str) -> Optional[AccountV1]:
        criteria = {
            '$or': [
                {'_id': id_or_login},
                {'login': id_or_login}
            ]
        }

        item = self._collection.find_one(criteria)
        self._logger.trace(context, "Retrieved from %s by %s", self._collection.name, id_or_login)
        item = self._convert_to_public(item)

        return item

    def create(self, context: Optional[IContext], item: AccountV1) -> AccountV1:
        if item is None:
            return None

        item.active = getattr(item, 'active', True)
        item.create_time = getattr(item, 'create_time', None) or datetime.utcnow()

        return super().create(context, item)
