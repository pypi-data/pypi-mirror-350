# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from typing import Optional

from pip_services4_components.context import IContext
from pip_services4_data.query import FilterParams, PagingParams, DataPage

from ..data.UserRolesV1 import UserRolesV1


class IRolesPersistence(ABC):
    @abstractmethod
    def get_page_by_filter(self, context: Optional[IContext], filter_params: FilterParams,
                           paging: PagingParams) -> DataPage:
        pass

    @abstractmethod
    def get_one_by_id(self, context: Optional[IContext], id: str) -> Optional[UserRolesV1]:
        pass

    @abstractmethod
    def set(self, context: Optional[IContext], item: UserRolesV1) -> UserRolesV1:
        pass
