# -*- coding: utf-8 -*-
from pip_services4_persistence.persistence import IdentifiableMemoryPersistence

from .IPasswordsPersistence import IPasswordsPersistence


class PasswordsMemoryPersistence(IdentifiableMemoryPersistence, IPasswordsPersistence):

    def __init__(self):
        super().__init__()