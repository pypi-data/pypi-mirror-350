# -*- coding: utf-8 -*-
from datetime import datetime
from typing import Optional
from pymongo import ReturnDocument

from pip_services4_components.context import IContext
from pip_services4_components.config import ConfigParams
from pip_services4_data.query import FilterParams, PagingParams, DataPage
from pip_services4_mongodb.persistence import IdentifiableMongoDbPersistence

from ..data.SettingsSectionV1 import SettingsSectionV1
from .ISettingsPersistence import ISettingsPersistence


class SettingsMongoDbPersistence(IdentifiableMongoDbPersistence, ISettingsPersistence):

    def __init__(self):
        super().__init__('settings')

    def _map_from_public(self, params: dict) -> dict:
        result = {}
        for key, value in params.items():
            new_key = key.replace('.', '_dot_')
            result[new_key] = value
        return result

    def _map_to_public(self, params: dict) -> dict:
        result = {}
        for key, value in params.items():
            new_key = key.replace('_dot_', '.')
            result[new_key] = value
        return result

    def convert_to_public(self, value: any) -> any:
        if value is None:
            return None
        return SettingsSectionV1(
            id=value.get('_id'),
            parameters=ConfigParams.from_value(self._map_to_public(value.get('parameters', {})))
        )

    def convert_from_public(self, item: SettingsSectionV1) -> any:
        return {
            '_id': item.id,
            'parameters': self._map_from_public(item.parameters.get_as_object()),
            'update_time': item.update_time
        }

    def _compose_filter(self, filter_params: FilterParams) -> dict:
        filter_params = filter_params or FilterParams()
        criteria = []

        if search := filter_params.get_as_nullable_string('search'):
            regex = {'$regex': search, '$options': 'i'}
            criteria.append({'_id': regex})

        if id := filter_params.get_as_nullable_string('id'):
            criteria.append({'_id': id})

        if id_starts := filter_params.get_as_nullable_string('id_starts'):
            regex = {'$regex': f'^{id_starts}', '$options': 'i'}
            criteria.append({'_id': regex})

        return {'$and': criteria} if criteria else {}

    def get_page_by_filter(self, context: Optional[IContext], filter_params: FilterParams,
                           paging: PagingParams) -> DataPage:
        return super().get_page_by_filter(context, self._compose_filter(filter_params), paging, None, None)

    def set(self, context: Optional[IContext], item: SettingsSectionV1) -> SettingsSectionV1:
        item.update_time = datetime.now()
        update = {
            '$set': {
                'parameters': self._map_from_public(item.parameters.get_as_object()),
                'update_time': item.update_time
            }
        }

        result = self._collection.find_one_and_update(
            {'_id': item.id}, update,
            return_document=ReturnDocument.AFTER,
            upsert=True
        )

        self._logger.trace(context, "Set settings with id=%s", item.id)
        return self.convert_to_public(result)

    def modify(self, context: Optional[IContext], id: str,
               update_params: ConfigParams, increment_params: ConfigParams) -> SettingsSectionV1:
        update = {'$set': {'update_time': datetime.now()}}

        if update_params:
            for key, value in update_params.items():
                mongo_key = 'parameters.' + key.replace('.', '_dot_')
                update['$set'][mongo_key] = value

        if increment_params:
            update['$inc'] = {}
            for key, inc in increment_params.items():
                mongo_key = 'parameters.' + key.replace('.', '_dot_')
                update['$inc'][mongo_key] = int(inc)

        result = self._collection.find_one_and_update(
            {'_id': id},
            update,
            return_document=ReturnDocument.AFTER,
            upsert=True
        )

        self._logger.trace(context, "Modified settings with id=%s", id)
        return self.convert_to_public(result)
    
    def get_one_by_id(self, context: Optional[IContext], id: str) -> Optional[SettingsSectionV1]:
        item = self._collection.find_one({'_id': id})
        if item:
            self._logger.trace(context, "Nothing found from %s with id = %s", self._collection_name, id)
        else:
            self._logger.trace(context, "Retrieved from %s with id = %s", self._collection_name, id)

        item = self.convert_to_public(item)
        return item
