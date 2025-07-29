# -*- coding: utf-8 -*-
from typing import Optional, Callable, Any
from datetime import datetime

from pip_services4_components.context import IContext
from pip_services4_data.query import FilterParams, PagingParams, DataPage
from pip_services4_persistence.persistence import IdentifiableMemoryPersistence

from ..data.UserRolesV1 import UserRolesV1
from .IRolesPersistence import IRolesPersistence


class RolesMemoryPersistence(IdentifiableMemoryPersistence, IRolesPersistence):
    def __init__(self):
        super().__init__()

    def __contains_any(self, array1, array2):
        if not array1 or not array2:
            return False
        return any(item in array2 for item in array1)

    def __compose_filter(self, filter_params: FilterParams) -> Callable[[UserRolesV1], bool]:
        filter_params = filter_params or FilterParams()

        id = filter_params.get_as_nullable_string('id')
        ids = filter_params.get_as_object('ids')
        except_ids = filter_params.get_as_object('except_ids')
        roles = filter_params.get_as_object('roles')
        except_roles = filter_params.get_as_object('except_roles')

        if isinstance(ids, str):
            ids = ids.split(',')
        if not isinstance(ids, list):
            ids = None

        if isinstance(except_ids, str):
            except_ids = except_ids.split(',')
        if not isinstance(except_ids, list):
            except_ids = None

        if isinstance(roles, str):
            roles = roles.split(',')
        if not isinstance(roles, list):
            roles = None

        if isinstance(except_roles, str):
            except_roles = except_roles.split(',')
        if not isinstance(except_roles, list):
            except_roles = None

        def filter_func(item: UserRolesV1) -> bool:
            if id and item.id != id:
                return False
            if ids and item.id not in ids:
                return False
            if except_ids and item.id in except_ids:
                return False
            if roles and not self.__contains_any(roles, item.roles):
                return False
            if except_roles and self.__contains_any(except_roles, item.roles):
                return False
            return True

        return filter_func

    def get_page_by_filter(self, context: Optional[IContext], filter_params: FilterParams,
                           paging: PagingParams) -> DataPage:
        return super().get_page_by_filter(context, self.__compose_filter(filter_params), paging)

    def get_one_by_id(self, context: Optional[IContext], id: str) -> Optional[UserRolesV1]:
        return super().get_one_by_id(context, id)

    def set(self, context: Optional[IContext], item: UserRolesV1) -> UserRolesV1:
        item.update_time = datetime.utcnow()
        return super().set(context, item)
