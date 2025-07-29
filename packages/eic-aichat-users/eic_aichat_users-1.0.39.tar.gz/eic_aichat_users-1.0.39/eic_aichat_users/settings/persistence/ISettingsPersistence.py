# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from typing import Optional
from pip_services4_components.context import IContext
from pip_services4_data.query import FilterParams, PagingParams, DataPage
from pip_services4_components.config import ConfigParams

from ..data.SettingsSectionV1 import SettingsSectionV1


class ISettingsPersistence(ABC):
    @abstractmethod
    def get_page_by_filter(self, context: Optional[IContext], filter_params: FilterParams,
                           paging: PagingParams) -> DataPage:
        pass

    @abstractmethod
    def get_one_by_id(self, context: Optional[IContext], id: str) -> Optional[SettingsSectionV1]:
        pass

    @abstractmethod
    def set(self, context: Optional[IContext], item: SettingsSectionV1) -> SettingsSectionV1:
        pass

    @abstractmethod
    def modify(self, context: Optional[IContext], id: str,
               update_params: ConfigParams, increment_params: ConfigParams) -> SettingsSectionV1:
        pass
