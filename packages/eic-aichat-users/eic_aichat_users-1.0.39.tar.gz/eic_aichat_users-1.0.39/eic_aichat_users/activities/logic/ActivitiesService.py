# -*- coding: utf-8 -*-
from typing import Optional, List

from pip_services4_components.context import IContext
from pip_services4_components.refer import IReferenceable, IReferences, Descriptor
from pip_services4_data.query import FilterParams, PagingParams, DataPage
from pip_services4_rpc.commands import CommandSet, ICommandable

from ..data import PartyActivityV1
from ..persistence import IActivitiesPersistence

from .ActivitiesCommandSet import ActivitiesCommandSet
from .IActivitiesService import IActivitiesService

class ActivitiesService(IActivitiesService, IReferenceable, ICommandable):
    _persistence: IActivitiesPersistence = None
    __command_set: ActivitiesCommandSet = None

    def set_references(self, references: IReferences):
        self._persistence = references.get_one_required(
            Descriptor('aichatusers-activities', 'persistence', '*', '*', '1.0')
        )

    def get_command_set(self) -> CommandSet:
        if self.__command_set is None:
            self.__command_set = ActivitiesCommandSet(self)

        return self.__command_set

    def get_activities(self, context: IContext, filter_params: FilterParams, paging_params: PagingParams) -> DataPage:
        return self._persistence.get_page_by_filter(context, filter_params, paging_params)

    def log_activity(self, context: IContext, activity: PartyActivityV1) -> PartyActivityV1:
        return self._persistence.create(context, activity)

    def batch_log_activities(self, context: IContext, activities: List[PartyActivityV1]) -> None:
        if activities is None or len(activities) == 0:
            return

        for activity in activities:
            self._persistence.create(context, activity)

    def delete_activities_by_filter(self, context: IContext, filter_params: FilterParams) -> None:
        self._persistence.delete_by_filter(context, filter_params)