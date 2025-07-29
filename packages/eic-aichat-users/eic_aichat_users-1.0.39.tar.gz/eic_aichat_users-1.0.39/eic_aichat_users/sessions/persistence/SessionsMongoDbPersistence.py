# -*- coding: utf-8 -*-
from datetime import datetime
from typing import Optional

from pip_services4_data.query import FilterParams, PagingParams, DataPage
from pip_services4_components.context import IContext
from pip_services4_mongodb.persistence import IdentifiableMongoDbPersistence

from ..data import SessionV1
from .ISessionsPersistence import ISessionsPersistence


class SessionsMongoDbPersistence(IdentifiableMongoDbPersistence, ISessionsPersistence):
    def __init__(self):
        super().__init__('sessions')

    def _compose_filter(self, filter_params: Optional[FilterParams]) -> dict:
        filter_params = filter_params or FilterParams()
        criteria = []

        id = filter_params.get_as_nullable_string('id')
        if id:
            criteria.append({'_id': id})

        user_id = filter_params.get_as_nullable_string('user_id')
        if user_id:
            criteria.append({'user_id': user_id})

        active = filter_params.get_as_nullable_boolean('active')
        if active is not None:
            criteria.append({'active': active})

        from_time = filter_params.get_as_nullable_datetime('from_time')
        if from_time:
            criteria.append({'request_time': {'$gte': from_time}})

        to_time = filter_params.get_as_nullable_datetime('to_time')
        if to_time:
            criteria.append({'request_time': {'$lt': to_time}})

        return {'$and': criteria} if criteria else {}

    def get_page_by_filter(self, context: Optional[IContext], filter_params: FilterParams,
                           paging: PagingParams) -> DataPage:
        return super().get_page_by_filter(context, self._compose_filter(filter_params), paging, sort={'request_time': -1})

    def create(self, context: Optional[IContext], item: SessionV1) -> SessionV1:
        now = datetime.utcnow()
        item.open_time = now
        item.request_time = now
        return super().create(context, item)

    def update(self, context: Optional[IContext], item: SessionV1) -> SessionV1:
        item.request_time = datetime.utcnow()
        return super().update(context, item)

    def close_expired(self, context: Optional[IContext], request_time: datetime):
        criteria = {'request_time': {'$lt': request_time}, 'active': True}
        update = {
            '$set': {
                'active': False,
                'request_time': datetime.utcnow(),
                'close_time': datetime.utcnow(),
                'user': None,
                'data': None
            }
        }
        result = self._collection.update_many(criteria, update)
        if result.modified_count > 0:
            self._logger.debug(context, f'Closed {result.modified_count} expired sessions')
