# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from typing import Optional

from pip_services4_components.context import IContext
from pip_services4_data.query import FilterParams, PagingParams, DataPage

from ..data import PartyActivityV1


class IActivitiesPersistence(ABC):
    """
    Interface for party activities persistence.
    """
    
    @abstractmethod
    def get_page_by_filter(self, context: IContext, filter_params: FilterParams, paging_params: PagingParams) -> DataPage:
        """
        Gets a page of party activities by specified filter
        
        Args:
            context: Operation context
            filter_params: Filter parameters
            paging_params: Paging parameters
            
        Returns:
            DataPage with retrieved party activities
        """
        pass

    @abstractmethod
    def get_one_by_id(self, context: IContext, id: str) -> Optional[PartyActivityV1]:
        """
        Gets party activity by id
        
        Args:
            context: Operation context
            id: Activity id
            
        Returns:
            Retrieved party activity
        """
        pass

    @abstractmethod
    def create(self, context: IContext, item: PartyActivityV1) -> PartyActivityV1:
        """
        Creates party activity
        
        Args:
            context: Operation context
            item: Party activity to create
            
        Returns:
            Created party activity
        """
        pass

    @abstractmethod
    def delete_by_id(self, context: IContext, id: str) -> Optional[PartyActivityV1]:
        """
        Deletes party activity by id
        
        Args:
            context: Operation context
            id: Activity id
            
        Returns:
            Deleted party activity
        """
        pass

    @abstractmethod
    def delete_by_filter(self, context: IContext, filter_params: FilterParams) -> None:
        """
        Deletes party activities by filter
        
        Args:
            context: Operation context
            filter_params: Filter parameters
        """
        pass 