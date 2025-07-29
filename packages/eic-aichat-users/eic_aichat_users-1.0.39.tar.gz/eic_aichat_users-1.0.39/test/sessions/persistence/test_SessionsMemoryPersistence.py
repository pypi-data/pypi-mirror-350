# -*- coding: utf-8 -*-
from eic_aichat_users.sessions.persistence.SessionsMemoryPersistence import SessionsMemoryPersistence
from test.sessions.persistence.SessionsPersistenceFixture import SessionsPersistenceFixture


class TestSessionsMemoryPersistence:
    persistence: SessionsMemoryPersistence
    fixture: SessionsPersistenceFixture

    def setup_method(self):
        self.persistence = SessionsMemoryPersistence()
        self.fixture = SessionsPersistenceFixture(self.persistence)

        self.persistence.open(None)
        self.persistence.clear(None)

    def teardown_method(self):
        self.persistence.close(None)

    def test_crud_operations(self):
        self.fixture.test_crud_operations()

    def test_get_with_filter(self):
        self.fixture.test_close_expired()
