# -*- coding: utf-8 -*-
from datetime import datetime
from typing import Callable, Optional
from pip_services4_components.context import IContext
from pip_services4_data.query import FilterParams, PagingParams, DataPage
from pip_services4_components.config import ConfigParams
from pip_services4_persistence.persistence import IdentifiableMemoryPersistence

from ..data.SettingsSectionV1 import SettingsSectionV1
from .ISettingsPersistence import ISettingsPersistence


class SettingsMemoryPersistence(IdentifiableMemoryPersistence, ISettingsPersistence):

    def __init__(self):
        super().__init__()

    def __compose_filter(self, filter_params: FilterParams) -> Callable[[SettingsSectionV1], bool]:
        filter_params = filter_params or FilterParams()
        search = filter_params.get_as_nullable_string('search')
        id = filter_params.get_as_nullable_string('id')
        id_starts = filter_params.get_as_nullable_string('id_starts')

        def filter_fn(item: SettingsSectionV1) -> bool:
            if search and search.lower() not in (item.id or '').lower():
                return False
            if id and item.id != id:
                return False
            if id_starts and not (item.id or '').startswith(id_starts):
                return False
            return True

        return filter_fn

    def get_page_by_filter(self, context: Optional[IContext], filter_params: FilterParams,
                           paging: PagingParams) -> DataPage:
        return super().get_page_by_filter(context, self.__compose_filter(filter_params), paging, None, None)

    def set(self, context: Optional[IContext], item: SettingsSectionV1) -> SettingsSectionV1:
        item.update_time = item.update_time or datetime.now()
        return super().set(context, item)

    def modify(self, context: Optional[IContext], id: str,
               update_params: ConfigParams, increment_params: ConfigParams) -> SettingsSectionV1:
        index = next((i for i, x in enumerate(self._items) if x.id == id), -1)
        item = self._items[index] if index >= 0 else SettingsSectionV1(id)

        if update_params:
            for key, value in update_params.items():
                item.parameters.set_as_object(key, value)

        if increment_params:
            for key, inc in increment_params.items():
                current = item.parameters.get_as_long_with_default(key, 0)
                item.parameters.set_as_object(key, current + int(inc))

        item.update_time = datetime.now()

        if index < 0:
            self._items.append(item)

        self._logger.trace(context, "Modified item with id=%s", id)
        self.save(context)
        return item
