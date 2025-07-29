# -*- coding: utf-8 -*-
from eic_aichat_users.settings.persistence.SettingsMemoryPersistence import SettingsMemoryPersistence
from test.settings.persistence.SettingsPersistenceFixture import SettingsPersistenceFixture


class TestSettingsMemoryPersistence:
    persistence: SettingsMemoryPersistence
    fixture: SettingsPersistenceFixture

    def setup_method(self):
        self.persistence = SettingsMemoryPersistence()
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
