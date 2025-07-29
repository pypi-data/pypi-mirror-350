# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from typing import Optional

from pip_services4_components.context import IContext

from ..data.version1.UserPasswordV1 import UserPasswordV1


class IPasswordsPersistence(ABC):

    @abstractmethod
    def get_one_by_id(self, context: Optional[IContext], id: str) -> Optional[UserPasswordV1]:
        pass

    @abstractmethod
    def create(self, context: Optional[IContext], item: UserPasswordV1) -> UserPasswordV1:
        pass

    @abstractmethod
    def update(self, context: Optional[IContext], item: UserPasswordV1) -> UserPasswordV1:
        pass

    @abstractmethod
    def delete_by_id(self, context: Optional[IContext], id: str) -> Optional[UserPasswordV1]:
        pass
