# -*- coding: utf-8 -*-
from typing import Any, Optional
from datetime import datetime

from pip_services4_data.data import IStringIdentifiable
from pip_services4_data.keys import IdGenerator


class AccountV1(IStringIdentifiable):
    def __init__(
        self,
        id: Optional[str] = None,
        login: Optional[str] = None,
        name: Optional[str] = None,
        language: Optional[str] = None,
        theme: Optional[str] = None,
        time_zone: Optional[str] = None
    ):
        self.id: str = id or IdGenerator.next_long()
        self.login: Optional[str] = login
        self.name: Optional[str] = name

        # Activity tracking
        self.create_time: datetime = datetime.utcnow()
        self.deleted: Optional[bool] = False
        self.active: bool = True

        # User preferences
        self.about: Optional[str] = None
        self.time_zone: Optional[str] = time_zone
        self.language: Optional[str] = language
        self.theme: Optional[str] = theme

        # Custom fields
        self.custom_hdr: Optional[Any] = None
        self.custom_dat: Optional[Any] = None

    def to_dict(self):
        return self.__dict__
