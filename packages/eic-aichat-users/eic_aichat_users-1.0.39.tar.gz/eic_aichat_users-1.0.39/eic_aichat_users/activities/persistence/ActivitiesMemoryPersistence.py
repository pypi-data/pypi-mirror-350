# -*- coding: utf-8 -*-
from typing import List, Optional

from pip_services4_components.context import IContext
from pip_services4_data.query import FilterParams, PagingParams, DataPage
from pip_services4_persistence.persistence import IdentifiableMemoryPersistence

from ..data import PartyActivityV1


class ActivitiesMemoryPersistence(IdentifiableMemoryPersistence):
    """
    Memory persistence for party activities.
    """
    
    def __init__(self):
        super().__init__()
        self._max_page_size = 1000

    def __compose_filter(self, filter_params: FilterParams):
        filter_params = filter_params or FilterParams()
        
        id = filter_params.get_as_nullable_string('id')
        party_id = filter_params.get_as_nullable_string('party_id')
        ref_item_id = filter_params.get_as_nullable_string('ref_item_id')
        ref_parent_id = filter_params.get_as_nullable_string('ref_parent_id')
        ref_party_id = filter_params.get_as_nullable_string('ref_party_id')
        type = filter_params.get_as_nullable_string('type')
        
        def filter_activities(item: PartyActivityV1) -> bool:
            if id is not None and item.id != id:
                return False
                
            if party_id is not None and (item.party is None or item.party.id != party_id):
                return False
                
            if ref_item_id is not None and (item.ref_item is None or item.ref_item.id != ref_item_id):
                return False
                
            if ref_parent_id is not None:
                if item.ref_parents is None or len(item.ref_parents) == 0:
                    return False
                    
                found = False
                for ref_parent in item.ref_parents:
                    if ref_parent.id == ref_parent_id:
                        found = True
                        break
                        
                if not found:
                    return False
                    
            if ref_party_id is not None and (item.ref_party is None or item.ref_party.id != ref_party_id):
                return False
                
            if type is not None and item.type != type:
                return False
                
            return True
            
        return filter_activities

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
        return super().get_page_by_filter(context, self.__compose_filter(filter_params), paging_params)

    def delete_by_filter(self, context: IContext, filter_params: FilterParams) -> None:
        """
        Deletes party activities by filter
        
        Args:
            context: Operation context
            filter_params: Filter parameters
        """
        filter_function = self.__compose_filter(filter_params)
        
        items_to_remove = []
        for item in self._items:
            if filter_function(item):
                items_to_remove.append(item)
                
        for item in items_to_remove:
            self._items.remove(item) 