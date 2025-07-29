# sessions_memory_persistence.py
from typing import Optional
from datetime import datetime
from pip_services4_data.query import FilterParams, PagingParams, DataPage
from pip_services4_components.context import IContext
from pip_services4_observability.log import CompositeLogger
from pip_services4_persistence.persistence import IdentifiableMemoryPersistence
from .ISessionsPersistence import ISessionsPersistence

from ..data.SessionV1 import SessionV1

class SessionsMemoryPersistence(IdentifiableMemoryPersistence, ISessionsPersistence):
    def __init__(self):
        super().__init__()

    def _compose_filter(self, filter_params: FilterParams):
        filter_params = filter_params or FilterParams()

        id = filter_params.get_as_nullable_string('id')
        user_id = filter_params.get_as_nullable_string('user_id')
        active = filter_params.get_as_nullable_boolean('active')
        from_time = filter_params.get_as_nullable_datetime('from_time')
        to_time = filter_params.get_as_nullable_datetime('to_time')

        def predicate(item: SessionV1):
            if id and item.id != id:
                return False
            if user_id and item.user_id != user_id:
                return False
            if active is not None and item.active != active:
                return False
            if from_time and item.request_time < from_time:
                return False
            if to_time and item.request_time >= to_time:
                return False
            return True

        return predicate

    def get_page_by_filter(self, context: Optional[IContext], filter_params: FilterParams, paging: PagingParams) -> DataPage:
        return super().get_page_by_filter(context, self._compose_filter(filter_params), paging)

    def create(self, context: Optional[IContext], item: SessionV1) -> SessionV1:
        item.open_time = datetime.utcnow()
        item.request_time = item.open_time
        return super().create(context, item)

    def update(self, context: Optional[IContext], item: SessionV1) -> SessionV1:
        item.request_time = datetime.utcnow()
        return super().update(context, item)

    def close_expired(self, context: Optional[IContext], request_time: datetime):
        now = datetime.utcnow()
        count = 0
        for item in self._items:
            if item.active and item.request_time < request_time:
                item.active = False
                item.close_time = now
                item.request_time = now
                item.user = None
                item.data = None
                count += 1

        if count > 0:
            self._logger.debug(context, f'Closed {count} expired sessions')
