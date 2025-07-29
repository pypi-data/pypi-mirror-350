# sessions_service.py
from typing import Optional, Any
from datetime import datetime, timedelta

from pip_services4_components.config import ConfigParams, IConfigurable
from pip_services4_components.context import IContext
from pip_services4_components.refer import IReferenceable, IReferences, Descriptor
from pip_services4_data.query import FilterParams, PagingParams, DataPage
from pip_services4_observability.log import CompositeLogger

from ..data import SessionV1
from ..persistence.ISessionsPersistence import ISessionsPersistence

class SessionsService(IConfigurable, IReferenceable):
    def __init__(self):
        self._logger: CompositeLogger = CompositeLogger()
        self._persistence: Optional[ISessionsPersistence] = None
        self._expire_timeout = 24 * 3600  # default 24 hours in seconds

    def configure(self, config: ConfigParams):
        self._expire_timeout = config.get_as_integer_with_default("options.expire_timeout", self._expire_timeout)

    def set_references(self, references: IReferences):
        self._logger.set_references(references)
        self._persistence = references.get_one_required(
            Descriptor('aichatusers-sessions', 'persistence', '*', '*', '1.0')
        )

    def get_sessions(self, context: Optional[IContext], filter_params: FilterParams, paging: PagingParams) -> DataPage:
        return self._persistence.get_page_by_filter(context, filter_params, paging)

    def get_session_by_id(self, context: Optional[IContext], session_id: str) -> Optional[SessionV1]:
        return self._persistence.get_one_by_id(context, session_id)

    def open_session(self, context: Optional[IContext], user_id: str, user_name: str,
                     address: str, client: str, user: Any, data: Any) -> SessionV1:
        session = SessionV1(user_id=user_id, user_name=user_name, address=address, client=client)
        session.user = user
        session.data = data
        return self._persistence.create(context, session)

    def store_session_data(self, context: Optional[IContext], session_id: str, data: Any) -> Optional[SessionV1]:
        session = self._persistence.get_one_by_id(context, session_id)
        if session:
            session.data = data
            session.request_time = datetime.utcnow()
            return self._persistence.update(context, session)
        return None

    def update_session_user(self, context: Optional[IContext], session_id: str, user: Any) -> Optional[SessionV1]:
        session = self._persistence.get_one_by_id(context, session_id)
        if session:
            session.user = user
            session.request_time = datetime.utcnow()
            return self._persistence.update(context, session)
        return None

    def close_session(self, context: Optional[IContext], session_id: str) -> Optional[SessionV1]:
        session = self._persistence.get_one_by_id(context, session_id)
        if session:
            session.active = False
            session.close_time = datetime.utcnow()
            session.request_time = session.close_time
            session.user = None
            session.data = None
            return self._persistence.update(context, session)
        return None

    def close_expired_sessions(self, context: Optional[IContext]):
        request_time = datetime.utcnow() - timedelta(seconds=self._expire_timeout)
        self._persistence.close_expired(context, request_time)

    def delete_session_by_id(self, context: Optional[IContext], session_id: str) -> Optional[SessionV1]:
        return self._persistence.delete_by_id(context, session_id)
