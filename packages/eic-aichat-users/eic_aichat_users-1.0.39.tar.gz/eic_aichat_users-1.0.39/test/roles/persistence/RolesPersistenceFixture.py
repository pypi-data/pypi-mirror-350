# -*- coding: utf-8 -*-
from pip_services4_data.query import FilterParams
from eic_aichat_users.roles.data.UserRolesV1 import UserRolesV1
from eic_aichat_users.roles.persistence.IRolesPersistence import IRolesPersistence

ROLES = ['Role 1', 'Role 2', 'Role 3']


class RolesPersistenceFixture:
    def __init__(self, persistence: IRolesPersistence):
        assert persistence is not None
        self._persistence = persistence

    def test_get_and_set_roles(self):
        # Set roles
        roles = self._persistence.set(None, UserRolesV1('1', ROLES))
        assert len(roles.roles) == 3

        # Get by id
        roles = self._persistence.get_one_by_id(None, '1')
        assert roles is not None
        assert len(roles.roles) == 3

        # Filter by roles
        page = self._persistence.get_page_by_filter(
            None,
            FilterParams.from_tuples('roles', ['Role 1', 'Role X']),
            None
        )
        assert page is not None
        assert len(page.data) == 1
