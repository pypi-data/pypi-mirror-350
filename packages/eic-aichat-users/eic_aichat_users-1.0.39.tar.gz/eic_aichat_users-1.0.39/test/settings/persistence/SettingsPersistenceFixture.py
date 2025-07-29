# -*- coding: utf-8 -*-
from pip_services4_components.config import ConfigParams
from pip_services4_data.query import FilterParams, PagingParams

from eic_aichat_users.settings.data.SettingsSectionV1 import SettingsSectionV1
from eic_aichat_users.settings.persistence.ISettingsPersistence import ISettingsPersistence


class SettingsPersistenceFixture:
    def __init__(self, persistence: ISettingsPersistence):
        assert persistence is not None
        self._persistence = persistence

    def test_get_and_set(self):
        settings = self._persistence.set(
            None,
            SettingsSectionV1(
                id='test.1',
                parameters=ConfigParams.from_tuples(
                    'key1', 'value11',
                    'key2', 'value12'
                )
            )
        )

        assert settings is not None
        assert settings.id == 'test.1'
        assert settings.parameters.get_as_string('key1') == 'value11'

        settings = self._persistence.set(
            None,
            SettingsSectionV1(
                id='test.2',
                parameters=ConfigParams.from_tuples(
                    'key1', 'value21',
                    'key2', 'value22'
                )
            )
        )

        assert settings is not None
        assert settings.id == 'test.2'
        assert settings.parameters.get_as_string('key1') == 'value21'

        settings = self._persistence.get_one_by_id(None, 'test.1')

        assert settings is not None
        assert settings.id == 'test.1'
        assert settings.parameters.get_as_string('key1') == 'value11'

        page = self._persistence.get_page_by_filter(None, FilterParams.from_tuples('id_starts', 'test'), None)
        assert len(page.data) == 2

    def test_set_parameter(self):
        settings = self._persistence.modify(None, 'test.1', ConfigParams.from_tuples('key1', 'value11a'), None)
        assert settings.parameters.get_as_string('key1') == 'value11a'

        settings = self._persistence.modify(None, 'test.1', ConfigParams.from_tuples('key1', 'value11b'), None)
        assert settings.parameters.get_as_string('key1') == 'value11b'

        settings = self._persistence.get_one_by_id(None, 'test.1')
        assert settings.parameters.get_as_string('key1') == 'value11b'

        settings = self._persistence.modify(None, 'test.1', ConfigParams.from_tuples('key1.key11', 'value11a'), None)
        assert settings.parameters.get_as_string('key1.key11') == 'value11a'

    def test_increment_parameter(self):
        settings = self._persistence.modify(None, 'test.1', None, ConfigParams.from_tuples('key1', 1))
        assert settings.parameters.get_as_string('key1') == '1'

        settings = self._persistence.modify(None, 'test.1', None, ConfigParams.from_tuples('key1', 2))
        assert settings.parameters.get_as_string('key1') == '3'

        settings = self._persistence.get_one_by_id(None, 'test.1')
        assert settings.parameters.get_as_string('key1') == '3'

    def test_get_sections(self):
        settings = self._persistence.set(
            None,
            SettingsSectionV1(
                id='test.1',
                parameters=ConfigParams.from_tuples(
                    'key1', 'value11',
                    'key2', 'value12'
                )
            )
        )

        assert settings.id == 'test.1'
        assert settings.parameters.get_as_string('key1') == 'value11'

        page = self._persistence.get_page_by_filter(None, FilterParams(), PagingParams(0, 10, True))
        assert len(page.data) == 1
