# -*- coding: utf-8 -*-
from typing import Optional
from datetime import datetime

from pip_services4_components.context import IContext
from pip_services4_data.query import FilterParams, PagingParams, DataPage
from pip_services4_mongodb.persistence import IdentifiableMongoDbPersistence

from ..data.UserRolesV1 import UserRolesV1
from .IRolesPersistence import IRolesPersistence


class RolesMongoDbPersistence(IdentifiableMongoDbPersistence, IRolesPersistence):
    def __init__(self):
        super().__init__('user_roles')

    def __compose_filter(self, filter_params: FilterParams):
        filter_params = filter_params or FilterParams()
        criteria = []

        id = filter_params.get_as_nullable_string('id')
        if id is not None:
            criteria.append({'_id': id})

        ids = filter_params.get_as_object('ids')
        if isinstance(ids, str):
            ids = ids.split(',')
        if isinstance(ids, list):
            criteria.append({'_id': {'$in': ids}})

        except_ids = filter_params.get_as_object('except_ids')
        if isinstance(except_ids, str):
            except_ids = except_ids.split(',')
        if isinstance(except_ids, list):
            criteria.append({'_id': {'$nin': except_ids}})

        roles = filter_params.get_as_object('roles')
        if isinstance(roles, str):
            roles = roles.split(',')
        if isinstance(roles, list):
            criteria.append({'roles': {'$in': roles}})

        except_roles = filter_params.get_as_object('except_roles')
        if isinstance(except_roles, str):
            except_roles = except_roles.split(',')
        if isinstance(except_roles, list):
            criteria.append({'roles': {'$nin': except_roles}})

        return {'$and': criteria} if criteria else None

    def get_page_by_filter(self, context: Optional[IContext], filter_params: FilterParams,
                           paging: PagingParams) -> DataPage:
        return super().get_page_by_filter(context, self.__compose_filter(filter_params), paging)

    def get_one_by_id(self, context: Optional[IContext], id: str) -> Optional[UserRolesV1]:
        return super().get_one_by_id(context, id)

    def set(self, context: Optional[IContext], item: UserRolesV1) -> UserRolesV1:
        item.update_time = datetime.utcnow()
        return super().set(context, item)
