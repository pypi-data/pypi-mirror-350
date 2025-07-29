# -*- coding: utf-8 -*-
from pip_services4_mongodb.persistence import IdentifiableMongoDbPersistence

from .IPasswordsPersistence import IPasswordsPersistence


class PasswordsMongoDbPersistence(IdentifiableMongoDbPersistence, IPasswordsPersistence):
    
    def __init__(self):
        super().__init__('passwords')
        self._max_page_size = 1000