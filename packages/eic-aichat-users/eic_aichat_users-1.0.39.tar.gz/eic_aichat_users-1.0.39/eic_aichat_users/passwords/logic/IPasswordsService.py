# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from typing import Optional

from pip_services4_components.context import IContext

from ..data.version1.UserPasswordInfoV1 import UserPasswordInfoV1


class IPasswordsService(ABC):

    @abstractmethod
    def get_password_info(self, context: Optional[IContext], user_id: str) -> UserPasswordInfoV1:
        raise NotImplementedError()

    @abstractmethod
    def validate_password(self, context: Optional[IContext], password: str) -> None:
        raise NotImplementedError()

    @abstractmethod
    def validate_password_for_user(self, context: Optional[IContext], user_id: str, password: str) -> None:
        raise NotImplementedError()

    @abstractmethod
    def set_password(self, context: Optional[IContext], user_id: str, password: str) -> None:
        raise NotImplementedError()

    @abstractmethod
    def set_temp_password(self, context: Optional[IContext], user_id: str) -> str:
        raise NotImplementedError()

    @abstractmethod
    def delete_password(self, context: Optional[IContext], user_id: str) -> None:
        raise NotImplementedError()

    @abstractmethod
    def authenticate(self, context: Optional[IContext], user_id: str, password: str) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def change_password(self, context: Optional[IContext], user_id: str, old_password: str, new_password: str) -> None:
        raise NotImplementedError()

    @abstractmethod
    def validate_code(self, context: Optional[IContext], user_id: str, code: str) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def reset_password(self, context: Optional[IContext], user_id: str, code: str, password: str) -> None:
        raise NotImplementedError()

    @abstractmethod
    def recover_password(self, context: Optional[IContext], user_id: str) -> None:
        raise NotImplementedError()
