# -*- coding: utf-8 -*-
import json

import bottle
from pip_services4_commons.convert import TypeCode
from pip_services4_components.refer import Descriptor, IReferences
from pip_services4_data.validate import ObjectSchema, ArraySchema
from pip_services4_http.controller import RestOperations, RestController
from pip_services4_components.context import Context

from eic_aichat_users.activities.data import PartyActivityV1, PartyActivityV1Schema
from eic_aichat_users.activities.logic.IActivitiesService import IActivitiesService
from eic_aichat_users.accounts.logic.IAccountsService import IAccountsService
from eic_aichat_users.partialfacade.operations.version1.Authorize import AuthorizerV1


class ActivitiesOperations(RestOperations):
    def __init__(self):
        super().__init__()
        self._activities_service: IActivitiesService = None
        self._dependency_resolver.put("activities-service", Descriptor('aichatusers-activities', 'service', '*', '*', '1.0'))

    def configure(self, config):
        super().configure(config)

    def set_references(self, references: IReferences):
        super().set_references(references)
        self._activities_service = self._dependency_resolver.get_one_required('activities-service')

    def get_activities(self):
        context = Context.from_trace_id(self._get_trace_id())
        self._logger.info(context, "----------get_activities() invoked")

        filter_params = self._get_filter_params()
        paging_params = self._get_paging_params()
        try:
            res = self._activities_service.get_activities(context, filter_params, paging_params)
            return self._send_result(res)
        except Exception as err:
            return self._send_error(err)
    
    def get_party_activities(self):
        context = Context.from_trace_id(self._get_trace_id())
        self._logger.info(context, "----------get_party_activities() invoked")

        filter_params = self._get_filter_params()
        paging_params = self._get_paging_params()
        party_id = self.get_param("party_id")
        filter_params.set_as_object("party_id", party_id)
        try:
            res = self._activities_service.get_activities(context, filter_params, paging_params)
            return self._send_result(res)
        except Exception as err:
            return self._send_error(err)

    def log_activity(self):
        context = Context.from_trace_id(self._get_trace_id())
        self._logger.info(context, "----------log_activity() invoked")

        activity = self._get_data()
        activity = None if not activity else PartyActivityV1(**activity)
        try:
            res = self._activities_service.log_activity(context, activity)
            return self._send_result(res)
        except Exception as err:
            return self._send_error(err)
        
    def log_activities(self):
        context = Context.from_trace_id(self._get_trace_id())
        self._logger.info(context, "----------log_activities() invoked")

        activities = self._get_data()
        activities = None if not activities else [PartyActivityV1(**activity) for activity in activities]
        try:
            res = self._activities_service.batch_log_activities(context, activities)
            return self._send_result(res)
        except Exception as err:
            return self._send_error(err)
    

    def register_routes(self, controller: RestController, auth: AuthorizerV1):
        pass
        # controller.register_route('get', 'users/activities', None, self.get_activities)

        # controller.register_route('get', 'users/<party_id>/activities', None, self.get_party_activities)

        # controller.register_route('post', 'users/activities', PartyActivityV1Schema(),
        #                           self.log_activity)
        
        # controller.register_route('post', 'users/activities/batch', ArraySchema(PartyActivityV1Schema()),
        #                           self.log_activities)

        
