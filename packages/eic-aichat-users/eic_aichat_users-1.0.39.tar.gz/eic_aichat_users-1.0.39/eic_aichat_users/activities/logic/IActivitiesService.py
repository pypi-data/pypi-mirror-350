# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from typing import Optional, List

from pip_services4_components.context import IContext
from pip_services4_data.query import FilterParams, PagingParams, DataPage

from ..data import PartyActivityV1


class IActivitiesService(ABC):
    @abstractmethod
    def get_activities(self, context: IContext, filter_params: FilterParams, paging_params: PagingParams) -> DataPage:
        pass

    @abstractmethod
    def log_activity(self, context: IContext, activity: PartyActivityV1) -> PartyActivityV1:
        pass

    @abstractmethod
    def batch_log_activities(self, context: IContext, activities: List[PartyActivityV1]) -> None:
        pass

    @abstractmethod
    def delete_activities_by_filter(self, context: IContext, filter_params: FilterParams) -> None:
        pass 