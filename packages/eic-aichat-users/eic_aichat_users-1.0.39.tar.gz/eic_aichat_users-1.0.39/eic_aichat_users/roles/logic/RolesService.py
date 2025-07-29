# -*- coding: utf-8 -*-
from typing import List, Optional

from pip_services4_components.config import ConfigParams, IConfigurable
from pip_services4_components.context import IContext
from pip_services4_components.refer import IReferenceable, IReferences, Descriptor
from pip_services4_data.query import FilterParams, PagingParams, DataPage

from ..data.UserRolesV1 import UserRolesV1
from ..persistence.IRolesPersistence import IRolesPersistence
from .IRolesService import IRolesService


class RolesService(IRolesService, IConfigurable, IReferenceable):
    _persistence: IRolesPersistence = None

    def configure(self, config: ConfigParams):
        pass  # No config needed yet

    def set_references(self, references: IReferences):
        self._persistence = references.get_one_required(
            Descriptor('aichatusers-roles', 'persistence', '*', '*', '1.0')
        )

    def get_roles_by_filter(self, context: Optional[IContext], filter_params: FilterParams,
                            paging: PagingParams) -> DataPage:
        return self._persistence.get_page_by_filter(context, filter_params, paging)

    def get_roles_by_id(self, context: Optional[IContext], user_id: str) -> Optional[List[str]]:
        roles = self._persistence.get_one_by_id(context, user_id)
        return roles.roles if roles else None

    def set_roles(self, context: Optional[IContext], user_id: str, roles: List[str]) -> List[str]:
        item = UserRolesV1(id=user_id, roles=roles)
        result = self._persistence.set(context, item)
        return result.roles if result else []

    def grant_roles(self, context: Optional[IContext], user_id: str, roles: List[str]) -> List[str]:
        if not roles:
            return []

        existing_roles = self.get_roles_by_id(context, user_id) or []

        # Add new roles avoiding duplicates
        updated_roles = list(set(existing_roles + roles))

        return self.set_roles(context, user_id, updated_roles)

    def revoke_roles(self, context: Optional[IContext], user_id: str, roles: List[str]) -> List[str]:
        if not roles:
            return []

        existing_roles = self.get_roles_by_id(context, user_id) or []

        # Remove specified roles
        updated_roles = [r for r in existing_roles if r not in roles]

        return self.set_roles(context, user_id, updated_roles)

    def authorize(self, context: Optional[IContext], user_id: str, roles: List[str]) -> bool:
        if not roles:
            return False

        existing_roles = self.get_roles_by_id(context, user_id) or []

        return all(role in existing_roles for role in roles)
