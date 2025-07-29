# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from typing import Optional
from pip_services4_components.context import IContext
from pip_services4_components.config import ConfigParams
from pip_services4_data.query import FilterParams, PagingParams, DataPage

from ..data.SettingsSectionV1 import SettingsSectionV1


class ISettingsService(ABC):

    @abstractmethod
    def get_section_ids(self, context: Optional[IContext], filter_params: FilterParams,
                        paging: PagingParams) -> DataPage[str]:
        pass

    @abstractmethod
    def get_sections(self, context: Optional[IContext], filter_params: FilterParams,
                     paging: PagingParams) -> DataPage:
        pass

    @abstractmethod
    def get_section_by_id(self, context: Optional[IContext], id: str) -> ConfigParams:
        pass

    @abstractmethod
    def set_section(self, context: Optional[IContext], id: str,
                    parameters: ConfigParams) -> ConfigParams:
        pass

    @abstractmethod
    def modify_section(self, context: Optional[IContext], id: str,
                       update_params: ConfigParams,
                       increment_params: ConfigParams) -> ConfigParams:
        pass
