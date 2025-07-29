# -*- coding: utf-8 -*-
import datetime
import os
import pytest

from pip_services4_components.config import ConfigParams
from pip_services4_components.context import Context
from pip_services4_data.query import FilterParams, PagingParams

from eic_aichat_users.activities.data import PartyActivityV1, ReferenceV1
from eic_aichat_users.activities.persistence import ActivitiesMongoDbPersistence
from test.activities.persistence.ActivitiesPersistenceFixture import ActivitiesPersistenceFixture

mongodb_uri = os.environ.get('MONGO_SERVICE_URI')
mongodb_host = os.environ.get('MONGO_SERVICE_HOST') or 'localhost'
mongodb_port = os.environ.get('MONGO_SERVICE_PORT') or 27017
mongodb_database = os.environ.get('MONGO_SERVICE_DB') or 'test'

@pytest.mark.skipif(not mongodb_uri and not mongodb_host, reason="MongoDB connection is not set")
class TestActivitiesMongoDbPersistence:
    persistence = None
    fixture = None

    def setup_method(self):
        self.persistence = ActivitiesMongoDbPersistence()
        self.persistence.configure(ConfigParams.from_tuples(
            'connection.uri', mongodb_uri,
            'connection.host', mongodb_host,
            'connection.port', mongodb_port,
            'connection.database', mongodb_database
        ))

        self.fixture = ActivitiesPersistenceFixture(self.persistence)

        self.persistence.open(None)
        self.persistence.clear(None)

    def teardown_method(self):
        self.persistence.close(None)

    def test_crud_operations(self):
        self.fixture.test_crud_operations()

    def test_get_with_filter(self):
        self.fixture.test_get_with_filter()