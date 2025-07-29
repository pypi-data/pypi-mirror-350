# -*- coding: utf-8 -*-
import json
import bottle
from typing import List

from pip_services4_commons.convert import TypeCode
from pip_services4_components.refer import Descriptor, IReferences
from pip_services4_data.validate import ObjectSchema
from pip_services4_http.controller import RestOperations, RestController
from pip_services4_components.context import Context

from eic_aichat_users.partialfacade.operations.version1.Authorize import AuthorizerV1
from eic_aichat_users.roles.logic.IRolesService import IRolesService
from eic_aichat_users.roles.data import UserRolesV1


class RolesOperations(RestOperations):
    def __init__(self):
        super().__init__()
        self._roles_service: IRolesService = None
        self._dependency_resolver.put("roles-service", Descriptor('aichatusers-roles', 'service', '*', '*', '1.0'))

    def configure(self, config):
        super().configure(config)

    def set_references(self, references: IReferences):
        super().set_references(references)
        self._roles_service = self._dependency_resolver.get_one_required("roles-service")

    def get_roles_by_filter(self):
        context = Context.from_trace_id(self._get_trace_id())
        self._logger.info(context, "----------get_roles_by_filter() invoked")

        filter_params = self._get_filter_params()
        paging_params = self._get_paging_params()
        try:
            res = self._roles_service.get_roles_by_filter(context, filter_params, paging_params)
            return self._send_result(res)
        except Exception as err:
            return self._send_error(err)

    def get_roles_by_id(self, user_id):
        context = Context.from_trace_id(self._get_trace_id())
        self._logger.info(context, "----------get_roles_by_id() invoked")

        try:
            res = self._roles_service.get_roles_by_id(context, user_id)
            return self._send_result(res)
        except Exception as err:
            return self._send_error(err)

    def set_roles(self, user_id):
        context = Context.from_trace_id(self._get_trace_id())
        self._logger.info(context, "----------set_roles() invoked")

        data = bottle.request.json or []
        try:
            res = self._roles_service.set_roles(context, user_id, data)
            return self._send_result(res)
        except Exception as err:
            return self._send_error(err)

    def grant_roles(self, user_id):
        context = Context.from_trace_id(self._get_trace_id())
        self._logger.info(context, "----------grant_roles() invoked")

        data = bottle.request.json or []
        try:
            res = self._roles_service.grant_roles(context, user_id, data)
            return self._send_result(res)
        except Exception as err:
            return self._send_error(err)

    def revoke_roles(self, user_id):
        context = Context.from_trace_id(self._get_trace_id())
        self._logger.info(context, "----------revoke_roles() invoked")

        data = bottle.request.json or []
        try:
            res = self._roles_service.revoke_roles(context, user_id, data)
            return self._send_result(res)
        except Exception as err:
            return self._send_error(err)

    def authorize(self, user_id):
        context = Context.from_trace_id(self._get_trace_id())
        self._logger.info(context, "----------authorize() invoked")

        data = bottle.request.json or []
        try:
            res = self._roles_service.authorize(context, user_id, data)
            return self._send_result(res)
        except Exception as err:
            return self._send_error(err)

    def register_routes(self, controller: RestController, auth: AuthorizerV1):
        # controller.register_route('get', '/roles', None, self.get_roles_by_filter)

        controller.register_route_with_auth('get', '/users/<user_id>/roles', ObjectSchema(True)
                                  .with_required_property("user_id", TypeCode.String), auth.owner_or_admin(), self.get_roles_by_id)

        # controller.register_route('post', '/roles/<user_id>/set', ObjectSchema(True)
        #                           .with_required_property("user_id", TypeCode.String)
        #                           .with_required_property("body", TypeCode.Array),
        #                           self.set_roles)

        controller.register_route_with_auth('post', '/users/<user_id>/roles/grant', ObjectSchema(True)
                                  .with_required_property("user_id", TypeCode.String)
                                  .with_required_property("body", TypeCode.Array), auth.admin(), self.grant_roles)

        controller.register_route_with_auth('post', '/users/<user_id>/roles/revoke', ObjectSchema(True)
                                  .with_required_property("user_id", TypeCode.String)
                                  .with_required_property("body", TypeCode.Array), auth.admin(), self.revoke_roles)

        # controller.register_route('post', '/roles/<user_id>/authorize', ObjectSchema(True)
        #                           .with_required_property("user_id", TypeCode.String)
        #                           .with_required_property("body", TypeCode.Array),
        #                           self.authorize)
