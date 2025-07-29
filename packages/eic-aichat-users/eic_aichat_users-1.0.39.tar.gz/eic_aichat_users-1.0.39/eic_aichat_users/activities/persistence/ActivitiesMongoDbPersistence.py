# -*- coding: utf-8 -*-
from typing import Optional

from pip_services4_components.context import IContext
from pip_services4_components.config import ConfigParams
from pip_services4_data.query import FilterParams, PagingParams, DataPage
from pip_services4_mongodb.persistence import IdentifiableMongoDbPersistence

from ..data import PartyActivityV1, ReferenceV1


class ActivitiesMongoDbPersistence(IdentifiableMongoDbPersistence):
    """
    MongoDB persistence for party activities.
    """

    def _convert_reference_from_public(self, reference: ReferenceV1) -> dict:
        if reference is None:
            return None
        return reference.__dict__

    def _convert_reference_to_public(self, reference: dict) -> ReferenceV1:
        if reference is None:
            return None
        return ReferenceV1(
            id=reference.get('id'),
            type=reference.get('type'),
            name=reference.get('name')
        )

    def _convert_from_public(self, item: PartyActivityV1) -> any:
        # return {
        #     '_id': item.id,
        #     'time': item.time,
        #     'party': self._convert_reference_from_public(item.party),
        #     'type': item.type,
        #     'ref_item': self._convert_reference_from_public(item.ref_item),
        #     'ref_parents': [self._convert_reference_from_public(ref_parent) for ref_parent in item.ref_parents],
        #     'ref_party': self._convert_reference_from_public(item.ref_party),
        #     'details': item.details
        # }
    
        result = item.__dict__.copy()
        result['_id'] = item.id

        if item.party:
            result['party'] = self._convert_reference_from_public(item.party)
        if item.ref_item:
            result['ref_item'] = self._convert_reference_from_public(item.ref_item)
        if item.ref_party:
            result['ref_party'] = self._convert_reference_from_public(item.ref_party)

        if item.ref_parents:
            result['ref_parents'] = [self._convert_reference_from_public(ref_parent) for ref_parent in item.ref_parents]

        return result

    def _convert_to_public(self, value: any) -> any:
        if value is None:
            return None
        
        return PartyActivityV1(
            id=value.get('_id'),
            time=value.get('time'),
            party=self._convert_reference_to_public(value.get('party')),
            type=value.get('type'),
            ref_item=self._convert_reference_to_public(value.get('ref_item')),
            ref_parents=[self._convert_reference_to_public(ref_parent) for ref_parent in value.get('ref_parents')],
            ref_party=self._convert_reference_to_public(value.get('ref_party')),
            details=value.get('details', {})
        )

    def __init__(self):
        """
        Creates a new instance of the persistence
        """
        super().__init__('activities')
        self._max_page_size = 1000

    def _compose_filter(self, filter_params: FilterParams):
        filter_params = filter_params or FilterParams()
        
        criteria = {}
        
        id = filter_params.get_as_nullable_string('id')
        if id is not None:
            criteria['_id'] = id
        
        ids = filter_params.get_as_nullable_string('ids')
        if ids is not None:
            criteria['ids'] = ids
            
        party_id = filter_params.get_as_nullable_string('party_id')
        if party_id is not None:
            criteria['party.id'] = party_id
            
        ref_item_id = filter_params.get_as_nullable_string('ref_item_id')
        if ref_item_id is not None:
            criteria['ref_item.id'] = ref_item_id
            
        ref_parent_id = filter_params.get_as_nullable_string('ref_parent_id')
        if ref_parent_id is not None:
            criteria['ref_parents.id'] = ref_parent_id
            
        ref_party_id = filter_params.get_as_nullable_string('ref_party_id')
        if ref_party_id is not None:
            criteria['ref_party.id'] = ref_party_id
            
        type = filter_params.get_as_nullable_string('type')
        if type is not None:
            criteria['type'] = type
            
        return criteria

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
        return super().get_page_by_filter(context, self._compose_filter(filter_params), paging_params, None, None)

    def delete_by_filter(self, context: IContext, filter_params: FilterParams) -> None:
        """
        Deletes party activities by filter
        
        Args:
            context: Operation context
            filter_params: Filter parameters
        """

        criteria = self._compose_filter(filter_params)
        return super().delete_by_ids(context, criteria.get('ids'))
    
    def create(self, context: IContext, item: PartyActivityV1) -> PartyActivityV1:
        if item is None:
            return

        new_item = self._convert_from_public(item)

        result = self._collection.insert_one(new_item)
        item = self._collection.find_one({'_id': result.inserted_id})

        item = self._convert_to_public(item)
        return item
        