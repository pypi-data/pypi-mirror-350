# -*- coding: utf-8 -*-
from pip_services4_components.refer import Descriptor
from pip_services4_components.build import Factory

from eic_aichat_users.accounts.logic.AccountsService import AccountsService
from eic_aichat_users.accounts.persistence.AccountsMemoryPersistence import AccountsMemoryPersistence
from eic_aichat_users.accounts.persistence.AccountsMongoDbPersistence import AccountsMongoDbPersistence

from eic_aichat_users.settings.logic.SettingsService import SettingsService
from eic_aichat_users.settings.persistence.SettingsMemoryPersistence import SettingsMemoryPersistence
from eic_aichat_users.settings.persistence.SettingsMongoDbPersistence import SettingsMongoDbPersistence

from eic_aichat_users.passwords.logic.PasswordsService import PasswordsService
from eic_aichat_users.passwords.persistence.PasswordsMemoryPersistence import PasswordsMemoryPersistence
from eic_aichat_users.passwords.persistence.PasswordsMongoDbPersistence import PasswordsMongoDbPersistence

from eic_aichat_users.activities.logic.ActivitiesService import ActivitiesService
from eic_aichat_users.activities.persistence.ActivitiesMemoryPersistence import ActivitiesMemoryPersistence
from eic_aichat_users.activities.persistence.ActivitiesMongoDbPersistence import ActivitiesMongoDbPersistence

from eic_aichat_users.roles.logic.RolesService import RolesService
from eic_aichat_users.roles.persistence.RolesMemoryPersistence import RolesMemoryPersistence
from eic_aichat_users.roles.persistence.RolesMongoDbPersistence import RolesMongoDbPersistence

from eic_aichat_users.sessions.logic.SessionsService import SessionsService
from eic_aichat_users.sessions.persistence.SessionsMemoryPersistence import SessionsMemoryPersistence
from eic_aichat_users.sessions.persistence.SessionsMongoDbPersistence import SessionsMongoDbPersistence


class AIChatUsersFactory(Factory):
    __AccountsMemoryPersistenceDescriptor = Descriptor('aichatusers-accounts', 'persistence', 'memory', '*', '1.0')
    __AccountsMongoDbPersistenceDescriptor = Descriptor('aichatusers-accounts', 'persistence', 'mongodb', '*', '1.0')
    __AccountsServiceDescriptor = Descriptor('aichatusers-accounts', 'service', 'default', '*', '1.0')

    __SettingsMemoryPersistenceDescriptor = Descriptor('aichatusers-settings', 'persistence', 'memory', '*', '1.0')
    __SettingsMongoDbPersistenceDescriptor = Descriptor('aichatusers-settings', 'persistence', 'mongodb', '*', '1.0')
    __SettingsServiceDescriptor = Descriptor('aichatusers-settings', 'service', 'default', '*', '1.0')

    __PasswordsMemoryPersistenceDescriptor = Descriptor('aichatusers-passwords', 'persistence', 'memory', '*', '1.0')
    __PasswordsMongoDbPersistenceDescriptor = Descriptor('aichatusers-passwords', 'persistence', 'mongodb', '*', '1.0')
    __PasswordsServiceDescriptor = Descriptor('aichatusers-passwords', 'service', 'default', '*', '1.0')

    __ActivitiesMemoryPersistenceDescriptor = Descriptor('aichatusers-activities', 'persistence', 'memory', '*', '1.0')
    __ActivitiesMongoDbPersistenceDescriptor = Descriptor('aichatusers-activities', 'persistence', 'mongodb', '*', '1.0')
    __ActivitiesServiceDescriptor = Descriptor('aichatusers-activities', 'service', 'default', '*', '1.0')

    __RolesMemoryPersistenceDescriptor = Descriptor('aichatusers-roles', 'persistence', 'memory', '*', '1.0')
    __RolesMongoDbPersistenceDescriptor = Descriptor('aichatusers-roles', 'persistence', 'mongodb', '*', '1.0')
    __RolesServiceDescriptor = Descriptor('aichatusers-roles', 'service', 'default', '*', '1.0')

    __SessionsMemoryPersistenceDescriptor = Descriptor('aichatusers-sessions', 'persistence', 'memory', '*', '1.0')
    __SessionsMongoDbPersistenceDescriptor = Descriptor('aichatusers-sessions', 'persistence', 'mongodb', '*', '1.0')
    __SessionsServiceDescriptor = Descriptor('aichatusers-sessions', 'service', 'default', '*', '1.0')


    def __init__(self):
        super().__init__()

        self.register_as_type(self.__AccountsMemoryPersistenceDescriptor, AccountsMemoryPersistence)
        self.register_as_type(self.__AccountsMongoDbPersistenceDescriptor, AccountsMongoDbPersistence)
        self.register_as_type(self.__AccountsServiceDescriptor, AccountsService)
        
        self.register_as_type(self.__SettingsMemoryPersistenceDescriptor, SettingsMemoryPersistence)
        self.register_as_type(self.__SettingsMongoDbPersistenceDescriptor, SettingsMongoDbPersistence)
        self.register_as_type(self.__SettingsServiceDescriptor, SettingsService)

        self.register_as_type(self.__PasswordsMemoryPersistenceDescriptor, PasswordsMemoryPersistence)
        self.register_as_type(self.__PasswordsMongoDbPersistenceDescriptor, PasswordsMongoDbPersistence)
        self.register_as_type(self.__PasswordsServiceDescriptor, PasswordsService)

        self.register_as_type(self.__ActivitiesMemoryPersistenceDescriptor, ActivitiesMemoryPersistence)
        self.register_as_type(self.__ActivitiesMongoDbPersistenceDescriptor, ActivitiesMongoDbPersistence)
        self.register_as_type(self.__ActivitiesServiceDescriptor, ActivitiesService)

        self.register_as_type(self.__RolesMemoryPersistenceDescriptor, RolesMemoryPersistence)
        self.register_as_type(self.__RolesMongoDbPersistenceDescriptor, RolesMongoDbPersistence)
        self.register_as_type(self.__RolesServiceDescriptor, RolesService)

        self.register_as_type(self.__SessionsMemoryPersistenceDescriptor, SessionsMemoryPersistence)
        self.register_as_type(self.__SessionsMongoDbPersistenceDescriptor, SessionsMongoDbPersistence)
        self.register_as_type(self.__SessionsServiceDescriptor, SessionsService)
