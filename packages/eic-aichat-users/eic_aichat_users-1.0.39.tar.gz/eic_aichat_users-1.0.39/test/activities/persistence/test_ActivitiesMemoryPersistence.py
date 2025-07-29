# -*- coding: utf-8 -*-
from eic_aichat_users.activities.persistence import ActivitiesMemoryPersistence
from test.activities.persistence.ActivitiesPersistenceFixture import ActivitiesPersistenceFixture


class TestActivitiesMemoryPersistence:
    persistence = None
    fixture = None

    @classmethod
    def setup_class(cls):
        cls.persistence = ActivitiesMemoryPersistence()
        cls.fixture = ActivitiesPersistenceFixture(cls.persistence)

    def setup_method(self, method):
        self.persistence.clear(None)

    def test_crud_operations(self):
        self.fixture.test_crud_operations()

    def test_get_with_filter(self):
        self.fixture.test_get_with_filter() 