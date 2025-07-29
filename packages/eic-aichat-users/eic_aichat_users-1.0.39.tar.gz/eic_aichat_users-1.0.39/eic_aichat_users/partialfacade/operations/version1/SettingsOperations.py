# -*- coding: utf-8 -*-
import json

import bottle
from pip_services4_commons.convert import TypeCode
from pip_services4_components.context import Context
from pip_services4_components.refer import Descriptor, IReferences
from pip_services4_data.validate import ObjectSchema
from pip_services4_http.controller import RestOperations, RestController
from pip_services4_components.config import ConfigParams

from eic_aichat_users.partialfacade.operations.version1.Authorize import AuthorizerV1
from eic_aichat_users.settings.logic.ISettingsService import ISettingsService
from eic_aichat_users.settings.data.SettingsSectionV1Schema import SettingsSectionV1Schema


class SettingsOperations(RestOperations):
    def __init__(self):
        super().__init__()
        self._settings_service: ISettingsService = None
        self._dependency_resolver.put("settings-service", Descriptor('aichatusers-settings', 'service', '*', '*', '1.0'))

    def configure(self, config):
        super().configure(config)

    def set_references(self, references: IReferences):
        super().set_references(references)
        self._settings_service = self._dependency_resolver.get_one_required('settings-service')

    def get_section_ids(self):
        context = Context.from_trace_id(self._get_trace_id())
        self._logger.info(context, "----------get_section_ids() invoked")

        filter_params = self._get_filter_params()
        paging_params = self._get_paging_params()
        try:
            res = self._settings_service.get_section_ids(context, filter_params, paging_params)
            return self._send_result(res)
        except Exception as err:
            return self._send_error(err)

    def get_sections(self):
        context = Context.from_trace_id(self._get_trace_id())
        self._logger.info(context, "----------get_sections() invoked")

        filter_params = self._get_filter_params()
        paging_params = self._get_paging_params()
        try:
            res = self._settings_service.get_sections(context, filter_params, paging_params)
            return self._send_result(res)
        except Exception as err:
            return self._send_error(err)

    def get_section_by_id(self, id):
        context = Context.from_trace_id(self._get_trace_id())
        self._logger.info(context, "----------get_section_by_id() invoked")

        try:
            res = self._settings_service.get_section_by_id(context, id)
            return self._send_result(res)
        except Exception as err:
            return self._send_error(err)

    def set_section(self):
        context = Context.from_trace_id(self._get_trace_id())
        self._logger.info(context, "----------set_section() invoked")

        data = bottle.request.json or {}
        id = data.get("id")
        parameters = ConfigParams.from_value(data.get("parameters") or {})
        try:
            res = self._settings_service.set_section(context, id, parameters)
            return self._send_result(res)
        except Exception as err:
            return self._send_error(err)

    def modify_section(self):
        context = Context.from_trace_id(self._get_trace_id())
        self._logger.info(context, "----------modify_section() invoked")

        data = bottle.request.json or {}
        id = data.get("id")
        update_params = ConfigParams.from_value(data.get("update_params") or {})
        increment_params = ConfigParams.from_value(data.get("increment_params") or {})
        try:
            res = self._settings_service.modify_section(context, id, update_params, increment_params)
            return self._send_result(res)
        except Exception as err:
            return self._send_error(err)


    # TODO: check AI Chat API Specs
    def register_routes(self, controller: RestController, auth: AuthorizerV1):
        controller.register_route_with_auth('get', 'users/<user_id>/settings/ids', None, auth.admin(), self.get_section_ids)

        controller.register_route_with_auth('get', 'users/<user_id>/settings', None, auth.admin(), self.get_sections)

        controller.register_route_with_auth('get', 'users/<user_id>/settings/<id>', ObjectSchema(True)
                                  .with_optional_property("id", TypeCode.String), 
                                  auth.owner_or_admin('id'), self.get_section_by_id)

        controller.register_route_with_auth('post', 'users/<user_id>/settings', ObjectSchema(True)
                                  .with_required_property("body", SettingsSectionV1Schema()), 
                                  auth.owner_or_admin('id'), self.set_section)

        controller.register_route_with_auth('post', 'users/<user_id>/settings/modify', ObjectSchema(True)
                                  .with_required_property("id", TypeCode.String)
                                  .with_optional_property("update_params", TypeCode.Map)
                                  .with_optional_property("increment_params", TypeCode.Map), 
                                  auth.owner_or_admin('id'), self.modify_section)
