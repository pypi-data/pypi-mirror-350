# -*- coding: utf-8 -*-
import os
import pytest
from pip_services4_components.config import ConfigParams

from eic_aichat_users.settings.persistence.SettingsMongoDbPersistence import SettingsMongoDbPersistence
from test.settings.persistence.SettingsPersistenceFixture import SettingsPersistenceFixture

mongodb_uri = os.environ.get('MONGO_SERVICE_URI')
mongodb_host = os.environ.get('MONGO_SERVICE_HOST') or 'localhost'
mongodb_port = os.environ.get('MONGO_SERVICE_PORT') or 27017
mongodb_database = os.environ.get('MONGO_SERVICE_DB') or 'test'


@pytest.mark.skipif(not mongodb_uri and not mongodb_host, reason="MongoDb connection is not set")
class TestSettingsMongoDbPersistence:
    persistence: SettingsMongoDbPersistence
    fixture: SettingsPersistenceFixture

    def setup_method(self):
        self.persistence = SettingsMongoDbPersistence()
        self.persistence.configure(ConfigParams.from_tuples(
            'connection.uri', mongodb_uri,
            'connection.host', mongodb_host,
            'connection.port', mongodb_port,
            'connection.database', mongodb_database,
        ))

        self.fixture = SettingsPersistenceFixture(self.persistence)

        self.persistence.open(None)
        self.persistence.clear(None)

    def teardown_method(self):
        self.persistence.close(None)

    def test_get_and_set(self):
        self.fixture.test_get_and_set()

    def test_set_parameter(self):
        self.fixture.test_set_parameter()

    def test_increment_parameter(self):
        self.fixture.test_increment_parameter()

    def test_get_sections(self):
        self.fixture.test_get_sections()
