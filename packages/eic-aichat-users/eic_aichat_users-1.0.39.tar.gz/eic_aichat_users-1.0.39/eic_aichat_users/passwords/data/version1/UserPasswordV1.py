# -*- coding: utf-8 -*-
from typing import Any, Optional
from datetime import datetime

from pip_services4_data.data import IStringIdentifiable
from pip_services4_data.keys import IdGenerator


class UserPasswordV1(IStringIdentifiable):
    def __init__(
            self,
            id: Optional[str] = None,
            password: Optional[str] = None,
    ):
        # Identification 
        self.id: str = id or IdGenerator.next_long()
        self.password: str = password

        # Password management
        self.change_time: Optional[datetime] = None
        self.locked: bool = False
        self.lock_time: Optional[datetime] = None
        self.fail_count: int = 0
        self.fail_time: Optional[datetime] = None
        self.rec_code: Optional[str] = None
        self.rec_expire_time: Optional[datetime] = None

        # Custom fields
        self.custom_hdr: Optional[Any] = None
        self.custom_dat: Optional[Any] = None

    def to_dict(self):
        return self.__dict__
