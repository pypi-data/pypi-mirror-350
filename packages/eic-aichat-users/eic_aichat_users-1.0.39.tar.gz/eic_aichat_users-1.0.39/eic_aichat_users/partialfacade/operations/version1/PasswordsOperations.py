# -*- coding: utf-8 -*-
from pip_services4_commons.convert import TypeCode
from pip_services4_components.refer import Descriptor, IReferences
from pip_services4_data.validate import ObjectSchema
from pip_services4_http.controller import RestOperations, RestController
from pip_services4_components.context import Context
import bottle

from eic_aichat_users.partialfacade.operations.version1.Authorize import AuthorizerV1
from eic_aichat_users.passwords.logic.IPasswordsService import IPasswordsService
from eic_aichat_users.accounts.logic.IAccountsService import IAccountsService

class PasswordsOperations(RestOperations):
    def __init__(self):
        super().__init__()
        self._passwords_service: IPasswordsService = None
        self._accounts_service: IAccountsService = None
        self._dependency_resolver.put("passwords-service", Descriptor('aichatusers-passwords', 'service', '*', '*', '1.0'))
        self._dependency_resolver.put("accounts-service", Descriptor('aichatusers-accounts', 'service', '*', '*', '1.0'))

    def configure(self, config):
        super().configure(config)

    def set_references(self, references: IReferences):
        super().set_references(references)
        self._passwords_service = self._dependency_resolver.get_one_required('passwords-service') 
        self._accounts_service = self._dependency_resolver.get_one_required('accounts-service')
        
    def change_password(self, user_id: str):
        context = Context.from_trace_id(self._get_trace_id())
        self._logger.info(context, "----------change_password() invoked")

        data = bottle.request.json or {}
        try:
            res = self._passwords_service.change_password(
                context, 
                user_id, 
                data.get("old_password"), 
                data.get("new_password")
                )
            return self._send_result(res)
        except Exception as err:
            return self._send_error(err)    
        
    def reset_password(self):
        context = Context.from_trace_id(self._get_trace_id())
        self._logger.info(context, "----------reset_password() invoked")

        data = bottle.request.json or {}
        try:
            account = self._accounts_service.get_account_by_id_or_login(context, data.get("login"))
            res = self._passwords_service.reset_password(
                context, 
                account.id, 
                data.get("code"), 
                data.get("password")
                )
            return self._send_result(res)
        except Exception as err:
            return self._send_error(err)  
        
    def recover_password(self):
        context = Context.from_trace_id(self._get_trace_id())
        self._logger.info(context, "----------recover_password() invoked")

        data = bottle.request.json or {}
        try:
            account = self._accounts_service.get_account_by_id_or_login(context, data.get("login"))
            res = self._passwords_service.recover_password(context, account.id)
            return self._send_result(res)
        except Exception as err:
            return self._send_error(err)   
        
    def register_routes(self, controller: RestController, auth: AuthorizerV1,):

        controller.register_route_with_auth('post', 'users/<user_id>/passwords/change', ObjectSchema(True)
                                  .with_required_property("user_id", TypeCode.String)
                                  .with_required_property("body", TypeCode.Map), auth.anybody(), self.change_password)

        controller.register_route_with_auth('post', 'users/passwords/reset', ObjectSchema(True)
                                  .with_required_property("body", TypeCode.Map), auth.anybody(), self.reset_password)
        
        controller.register_route_with_auth('post', 'users/passwords/recover', ObjectSchema(True)
                                  .with_required_property("body", TypeCode.Map), auth.anybody(), self.recover_password)


        