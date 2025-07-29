# -*- coding: utf-8 -*-
from datetime import datetime
from pip_services4_data.query import FilterParams, PagingParams
from eic_aichat_users.passwords.data.version1.UserPasswordV1 import UserPasswordV1
from eic_aichat_users.passwords.persistence.IPasswordsPersistence import IPasswordsPersistence


USER_PWD = UserPasswordV1('1', 'password123')


class PasswordsPersistenceFixture:
    _persistence: IPasswordsPersistence

    def __init__(self, persistence: IPasswordsPersistence):
        assert persistence is not None
        self._persistence = persistence

    def test_crud_operations(self):
        # Create user password
        user_password = self._persistence.create(None, USER_PWD)

        self._assert_is_object(user_password)
        assert user_password.id == USER_PWD.id
        assert user_password.password is not None
        assert user_password.locked is False

        # Update the user password
        user_password = UserPasswordV1(USER_PWD.id, 'newpwd123')
        user_password.rec_code = "123"
        user_password.rec_expire_time = datetime.utcnow()

        user_password = self._persistence.update(None, user_password)

        self._assert_is_object(user_password)
        assert user_password.id == USER_PWD.id
        assert user_password.password == 'newpwd123'

        # Get user password
        user_password = self._persistence.get_one_by_id(None, USER_PWD.id)

        self._assert_is_object(user_password)
        assert user_password.id == USER_PWD.id

        # Delete the user password
        self._persistence.delete_by_id(None, USER_PWD.id)

        # Try to get deleted user
        user_password = self._persistence.get_one_by_id(None, USER_PWD.id)
        assert user_password is None

    def _assert_is_object(self, obj):
        assert obj is not None and isinstance(obj, object)

