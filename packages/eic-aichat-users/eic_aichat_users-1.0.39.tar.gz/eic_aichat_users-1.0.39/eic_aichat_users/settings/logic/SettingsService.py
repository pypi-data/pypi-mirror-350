# -*- coding: utf-8 -*-
from typing import Optional
from pip_services4_components.context import IContext
from pip_services4_components.refer import IReferences, IReferenceable, Descriptor
from pip_services4_components.config import ConfigParams
from pip_services4_data.query import FilterParams, PagingParams, DataPage

from ..data.SettingsSectionV1 import SettingsSectionV1
from ..persistence.ISettingsPersistence import ISettingsPersistence
from .ISettingsService import ISettingsService


class SettingsService(ISettingsService, IReferenceable):
    __persistence: ISettingsPersistence = None

    def set_references(self, references: IReferences):
        self.__persistence = references.get_one_required(
            Descriptor('aichatusers-settings', 'persistence', '*', '*', '1.0')
        )

    def get_section_ids(self, context: Optional[IContext], filter_params: FilterParams,
                        paging: PagingParams) -> DataPage[str]:
        page = self.__persistence.get_page_by_filter(context, filter_params, paging)
        ids = [item.id for item in page.data]
        return DataPage(ids, page.total)

    def get_sections(self, context: Optional[IContext], filter_params: FilterParams,
                     paging: PagingParams) -> DataPage:
        return self.__persistence.get_page_by_filter(context, filter_params, paging)

    def get_section_by_id(self, context: Optional[IContext], id: str) -> ConfigParams:
        item = self.__persistence.get_one_by_id(context, id)
        return item.parameters if item else ConfigParams()

    def set_section(self, context: Optional[IContext], id: str,
                    parameters: ConfigParams) -> ConfigParams:
        item = SettingsSectionV1(id=id, parameters=parameters)
        item = self.__persistence.set(context, item)
        return item.parameters

    def modify_section(self, context: Optional[IContext], id: str,
                       update_params: ConfigParams,
                       increment_params: ConfigParams) -> ConfigParams:
        item = self.__persistence.modify(context, id, update_params, increment_params)
        return item.parameters
