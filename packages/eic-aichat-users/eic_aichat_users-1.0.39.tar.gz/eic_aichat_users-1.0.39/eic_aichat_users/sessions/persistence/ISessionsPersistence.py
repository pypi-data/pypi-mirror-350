# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from typing import Optional
from datetime import datetime

from pip_services4_components.context import IContext
from pip_services4_data.query import FilterParams, PagingParams, DataPage
from pip_services4_commons.data import AnyValueMap

from ..data import SessionV1


class ISessionsPersistence(ABC):

    @abstractmethod
    def get_page_by_filter(self, context: Optional[IContext], filter_params: FilterParams,
                           paging: PagingParams) -> DataPage:
        raise NotImplementedError()

    @abstractmethod
    def get_one_by_id(self, context: Optional[IContext], id: str) -> Optional[SessionV1]:
        raise NotImplementedError()

    @abstractmethod
    def create(self, context: Optional[IContext], item: SessionV1) -> SessionV1:
        raise NotImplementedError()

    @abstractmethod
    def update(self, context: Optional[IContext], item: SessionV1) -> SessionV1:
        raise NotImplementedError()

    @abstractmethod
    def update_partially(self, context: Optional[IContext], id: str, data: AnyValueMap) -> SessionV1:
        raise NotImplementedError()

    @abstractmethod
    def delete_by_id(self, context: Optional[IContext], id: str) -> Optional[SessionV1]:
        raise NotImplementedError()

    @abstractmethod
    def close_expired(self, context: Optional[IContext], request_time: datetime):
        raise NotImplementedError()
