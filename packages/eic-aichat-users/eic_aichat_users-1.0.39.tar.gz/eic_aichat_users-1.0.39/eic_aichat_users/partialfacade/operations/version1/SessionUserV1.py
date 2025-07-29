# -*- coding: utf-8 -*-
import datetime
from typing import List, Any


class SessionUserV1:
    def __init__(self, id: str = None, login: str = None, name: str = None, create_time: str = None,
                 time_zone: str = None, language: str = None,
                 theme: str = None, roles: List[str] = None, change_pwd_time: datetime.datetime = None,
                 sites: List[dict] = None, settings: Any = None, custom_hdr: Any = None,
                 custom_dat: Any = None):

        # Identification
        self.id = id
        self.login = login
        self.name = name
        self.create_time = create_time

        # User information
        self.time_zone = time_zone
        self.language = language
        self.theme = theme

        # Security info
        self.roles = roles
        self.change_pwd_time = change_pwd_time
        self.sites = sites
        self.settings = settings

        # Custom fields
        self.custom_hdr = custom_hdr
        self.custom_dat = custom_dat

    def to_dict(self):
        return {
            "id": self.id,
            "login": self.login,
            "name": self.name,
            "create_time": self.create_time,
            "time_zone": self.time_zone,
            "language": self.language,
            "theme": self.theme,
            "roles": self.roles,
            "change_pwd_time": self.change_pwd_time.isoformat() if self.change_pwd_time else None,
            "sites": self.sites,
            "settings": self.settings,
            "custom_hdr": self.custom_hdr,
            "custom_dat": self.custom_dat
        }
