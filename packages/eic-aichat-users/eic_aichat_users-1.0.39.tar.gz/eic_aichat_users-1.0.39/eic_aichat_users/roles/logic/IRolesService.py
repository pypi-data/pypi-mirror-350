# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from typing import List, Optional

from pip_services4_components.context import IContext
from pip_services4_data.query import FilterParams, PagingParams, DataPage

from ..data.UserRolesV1 import UserRolesV1


class IRolesService(ABC):

    @abstractmethod
    def get_roles_by_filter(self, context: Optional[IContext], filter_params: FilterParams,
                            paging: PagingParams) -> DataPage:
        raise NotImplementedError()

    @abstractmethod
    def get_roles_by_id(self, context: Optional[IContext], user_id: str) -> Optional[List[str]]:
        raise NotImplementedError()

    @abstractmethod
    def set_roles(self, context: Optional[IContext], user_id: str, roles: List[str]) -> List[str]:
        raise NotImplementedError()

    @abstractmethod
    def grant_roles(self, context: Optional[IContext], user_id: str, roles: List[str]) -> List[str]:
        raise NotImplementedError()

    @abstractmethod
    def revoke_roles(self, context: Optional[IContext], user_id: str, roles: List[str]) -> List[str]:
        raise NotImplementedError()

    @abstractmethod
    def authorize(self, context: Optional[IContext], user_id: str, roles: List[str]) -> bool:
        raise NotImplementedError()
