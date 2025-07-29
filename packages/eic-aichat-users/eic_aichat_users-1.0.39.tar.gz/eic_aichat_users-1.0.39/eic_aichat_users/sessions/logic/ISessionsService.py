# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from typing import Any, Optional

from pip_services4_components.context import IContext
from pip_services4_data.query import FilterParams, PagingParams, DataPage

from ..data import SessionV1


class ISessionsService(ABC):

    @abstractmethod
    def get_sessions(self, context: Optional[IContext], filter_params: FilterParams,
                     paging: PagingParams) -> DataPage:
        raise NotImplementedError()

    @abstractmethod
    def get_session_by_id(self, context: Optional[IContext], session_id: str) -> Optional[SessionV1]:
        raise NotImplementedError()

    @abstractmethod
    def open_session(self, context: Optional[IContext], user_id: str, user_name: str,
                     address: str, client: str, user: Any, data: Any) -> SessionV1:
        raise NotImplementedError()

    @abstractmethod
    def store_session_data(self, context: Optional[IContext], session_id: str, data: Any) -> SessionV1:
        raise NotImplementedError()

    @abstractmethod
    def update_session_user(self, context: Optional[IContext], session_id: str, user: Any) -> SessionV1:
        raise NotImplementedError()

    @abstractmethod
    def close_session(self, context: Optional[IContext], session_id: str) -> SessionV1:
        raise NotImplementedError()

    @abstractmethod
    def close_expired_sessions(self, context: Optional[IContext]):
        raise NotImplementedError()

    @abstractmethod
    def delete_session_by_id(self, context: Optional[IContext], session_id: str) -> SessionV1:
        raise NotImplementedError()
