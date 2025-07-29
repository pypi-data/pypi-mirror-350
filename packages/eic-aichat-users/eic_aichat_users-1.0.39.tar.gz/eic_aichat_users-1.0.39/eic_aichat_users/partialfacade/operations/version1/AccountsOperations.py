# -*- coding: utf-8 -*-
import json
from typing import Optional

import bottle
from pip_services4_commons.convert import TypeCode
from pip_services4_components.refer import Descriptor, IReferences
from pip_services4_data.validate import ObjectSchema
from pip_services4_http.controller import RestOperations, RestController
from pip_services4_components.context import Context
from pip_services4_commons.errors import UnauthorizedException

from eic_aichat_users.accounts.data import AccountV1, AccountV1Schema
from eic_aichat_users.accounts.logic.IAccountsService import IAccountsService
from eic_aichat_users.partialfacade.operations.version1.Authorize import AuthorizerV1
from eic_aichat_users.passwords.logic.IPasswordsService import IPasswordsService
from eic_aichat_users.sessions.logic.ISessionsService import ISessionsService
from eic_aichat_users.roles.logic.IRolesService import IRolesService


class AccountsOperations(RestOperations):
    def __init__(self):
        super().__init__()
        self._accounts_service: IAccountsService = None
        self._passwords_service: IPasswordsService = None
        self._sessions_service: ISessionsService = None
        self._roles_service: IRolesService = None
        self._dependency_resolver.put("accounts-service", Descriptor('aichatusers-accounts', 'service', '*', '*', '1.0'))
        self._dependency_resolver.put("passwords-service", Descriptor('aichatusers-passwords', 'service', '*', '*', '1.0'))
        self._dependency_resolver.put("sessions-service", Descriptor("aichatusers-sessions", "service", "*", "*", "1.0"))
        self._dependency_resolver.put("roles-service", Descriptor('aichatusers-roles', 'service', '*', '*', '1.0'))

    def configure(self, config):
        super().configure(config)

    def set_references(self, references: IReferences):
        super().set_references(references)
        self._accounts_service = self._dependency_resolver.get_one_required('accounts-service')
        self._passwords_service = self._dependency_resolver.get_one_required('passwords-service') 
        self._sessions_service = self._dependency_resolver.get_one_required("sessions-service")
        self._roles_service = self._dependency_resolver.get_one_required("roles-service")

    def get_accounts(self):
        context = Context.from_trace_id(self._get_trace_id())
        self._logger.info(context, "----------get_accounts() invoked")

        filter_params = self._get_filter_params()
        paging_params = self._get_paging_params()
        try:
            res = self._accounts_service.get_accounts(context, filter_params, paging_params)
            return self._send_result(res)
        except Exception as err:
            return self._send_error(err)

    def get_account_by_id(self, id):
        context = Context.from_trace_id(self._get_trace_id())
        self._logger.info(context, "----------get_account_by_id() invoked")

        try:
            res = self._accounts_service.get_account_by_id(context, id)
            return self._send_result(res)
        except Exception as err:
            return self._send_error(err)

    def get_account_by_login(self, login):
        context = Context.from_trace_id(self._get_trace_id())
        self._logger.info(context, "----------get_account_by_login() invoked")

        try:
            res = self._accounts_service.get_account_by_login(context, login)
            return self._send_result(res)
        except Exception as err:
            return self._send_error(err)

    def get_account_by_id_or_login(self, id_or_login):
        context = Context.from_trace_id(self._get_trace_id())
        self._logger.info(context, "----------get_account_by_id_or_login() invoked")

        try:
            res = self._accounts_service.get_account_by_id_or_login(context, id_or_login)
            return self._send_result(res)
        except Exception as err:
            return self._send_error(err)

    def create_account(self):
        context = Context.from_trace_id(self._get_trace_id())
        self._logger.info(context, "----------create_account() invoked")

        data = bottle.request.json

        account_data = dict(data)
        password = account_data.pop("password", None)

        account = None if not account_data else AccountV1(**account_data)
        try:

            self._logger.info(context, f"----------Create account: {account.__dict__}")
            # Create account
            res = self._accounts_service.create_account(context, account)

            self._logger.info(context, f"----------Create passwor: f{res.__dict__}")
            # Create password for the account
            if password is not None:
                self._passwords_service.set_password(context, res.id, password)
            else:
                pwd = self._passwords_service.set_temp_password(context, res.id)
                password = pwd

            if res is not None:
                result = self.serialize_account(res, password)
                self._logger.info(context, f"----------response: {result}")
                return self._send_result(result)

            self._logger.info(context, f"----------response: {res.__dict__}")

            return self._send_result(res)
        except Exception as err:
            self._logger.info(context, f"----------Exception: {err}")
            return self._send_error(err)

    # TODO: check
    def update_account(self, user_id):
        context = Context.from_trace_id(self._get_trace_id())
        self._logger.info(context, "----------update_account() invoked")
        
        # Retrieving and deserializing the request body
        data = bottle.request.json
        account_data = data if isinstance(data, dict) else json.loads(data or '{}')

        # Assign an ID to the account object
        account_data['id'] = user_id
        account = AccountV1(**account_data)

        try:
            # Account Update
            new_account: Optional[AccountV1] = self._accounts_service.update_account(context, account)

            # Updating session data, if applicable
            session_id = data.get("session_id")
            user_data = data.get("user")  

            if new_account and session_id and user_data and new_account.id == user_data.get('id'):
                # Merging new account data with the current user
                updated_user = {**user_data, **new_account.to_dict()}
                self._sessions_service.update_session_user(context, session_id, updated_user)

            return self._send_result(new_account if new_account else None, status=200 if new_account else 204)

        except Exception as err:
            return self._send_error(err)

    def delete_account_by_id(self, id):
        context = Context.from_trace_id(self._get_trace_id())
        self._logger.info(context, "----------delete_account_by_id() invoked")

        try:
            res = self._accounts_service.delete_account_by_id(context, id)
            roles = self._roles_service.get_roles_by_id(context, id)
            self._roles_service.revoke_roles(context, id, roles)
            return self._send_result(res)
        except Exception as err:
            return self._send_error(err)

    def drop_account_by_id(self, id):
        context = Context.from_trace_id(self._get_trace_id())
        self._logger.info(context, "----------drop_account_by_id() invoked")

        try:
            res = self._accounts_service.drop_account_by_id(context, id)
            return self._send_result(res)
        except Exception as err:
            return self._send_error(err)
        
    def serialize_account(self, account: AccountV1, password: str = None) -> dict:
        if account is None:
            return {}

        return {
            "id": account.id,
            "login": account.login,
            "name": account.name,
            "create_time": account.create_time.isoformat() if account.create_time else None,
            "deleted": account.deleted,
            "active": account.active,
            "about": account.about,
            "time_zone": account.time_zone,
            "language": account.language,
            "theme": account.theme,
            "custom_hdr": account.custom_hdr,
            "custom_dat": account.custom_dat,
            "password": password
        }
    
    def get_current_accounts(self):
        context = Context.from_trace_id(self._get_trace_id())
        self._logger.info(context, "----------get_current_accounts() invoked")
        
        user = getattr(bottle.request, 'user', None)
        if user is None:
            raise UnauthorizedException(
                None, 'NOT_SIGNED',
                'User must be signed in to perform this operation'
            ).with_status(401)
        try:
            res = self._accounts_service.get_account_by_id(context, user)
            return self._send_result(res)
        except Exception as err:
            return self._send_error(err)

    def register_routes(self, controller: RestController, auth: AuthorizerV1):
        controller.register_route_with_auth('get', '/users', None, auth.signed(), self.get_accounts)

        controller.register_route_with_auth('get', '/users/<id>', ObjectSchema(True)
                                  .with_optional_property("id", TypeCode.String), auth.owner_or_admin(), self.get_account_by_id)

        controller.register_route_with_auth('get', '/users/current', None, auth.signed(), self.get_current_accounts)

        # TODO: check AI Chat API Specs
        controller.register_route_with_auth('get', '/users/by_login/<login>', ObjectSchema(True)
                                  .with_optional_property("login", TypeCode.String), auth.owner_or_admin(), self.get_account_by_login)

        # TODO: check AI Chat API Specs
        controller.register_route_with_auth('get', '/users/by_id_or_login/<id_or_login>', ObjectSchema(True)
                                  .with_optional_property("id_or_login", TypeCode.String), auth.owner_or_admin(), self.get_account_by_id_or_login)

        controller.register_route_with_auth('post', '/users', ObjectSchema(True)
                                  .with_required_property("body", AccountV1Schema()), auth.admin(), self.create_account)

        controller.register_route_with_auth('put', '/users/<user_id>', ObjectSchema(True)
                                  .with_required_property("user_id", TypeCode.String)
                                  .with_required_property("body", AccountV1Schema()), auth.signed(), self.update_account)

        controller.register_route_with_auth('delete', '/users/<id>', ObjectSchema(True)
                                  .with_required_property("id", TypeCode.String), auth.admin(), self.delete_account_by_id)