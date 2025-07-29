# -*- coding: utf-8 -*-
import bottle

from typing import List
from pip_services4_components.refer import Descriptor, IReferences
from pip_services4_http.controller import RestOperations, RestController, HttpRequestDetector
from pip_services4_components.context import Context
from pip_services4_commons.convert import TypeCode, JsonConverter
from pip_services4_components.config import ConfigParams
from pip_services4_commons.errors import UnauthorizedException, BadRequestException

from eic_aichat_users.partialfacade.operations.version1.Authorize import AuthorizerV1
from eic_aichat_users.sessions.data import SessionV1
from eic_aichat_users.accounts.logic.IAccountsService import IAccountsService
from eic_aichat_users.accounts.data.AccountV1 import AccountV1
from eic_aichat_users.passwords.logic.IPasswordsService import IPasswordsService
from eic_aichat_users.sessions.logic.ISessionsService import ISessionsService
from eic_aichat_users.passwords.data.version1.UserPasswordInfoV1 import UserPasswordInfoV1
from eic_aichat_users.roles.logic.IRolesService import IRolesService
from eic_aichat_users.settings.logic.ISettingsService import ISettingsService

from .SessionUserV1 import SessionUserV1


class SessionsOperations(RestOperations):
    __default_config = ConfigParams.from_tuples(
        'options.cookie_enabled', True,
        'options.cookie', 'x-session-id',
        'options.max_cookie_age', 365 * 24 * 60 * 60 * 1000
    )
        
    def __init__(self):
        super().__init__()
        self.__cookie: str = 'x-session-id'
        self.__cookie_enabled: bool = True
        self.__max_cookie_age: float = 365 * 24 * 60 * 60 * 1000
        self._accounts_service: IAccountsService = None
        self._passwords_service: IPasswordsService = None
        self._sessions_service: ISessionsService = None
        self._roles_service: IRolesService = None
        self._settings_service: ISettingsService = None

        self._dependency_resolver.put("accounts-service", Descriptor('aichatusers-accounts', 'service', '*', '*', '1.0'))
        self._dependency_resolver.put("passwords-service", Descriptor('aichatusers-passwords', 'service', '*', '*', '1.0'))
        self._dependency_resolver.put("sessions-service", Descriptor("aichatusers-sessions", "service", "*", "*", "1.0"))
        self._dependency_resolver.put("roles-service", Descriptor('aichatusers-roles', 'service', '*', '*', '1.0'))
        self._dependency_resolver.put("settings-service", Descriptor('aichatusers-settings', 'service', '*', '*', '1.0'))

    def configure(self, config):
        config = config.set_defaults(self.__default_config)
        super().configure(config)
        self._dependency_resolver.configure(config)

        self.__cookie_enabled = config.get_as_boolean_with_default('options.cookie_enabled', self.__cookie_enabled)
        self.__cookie = config.get_as_string_with_default('options.cookie', self.__cookie)
        self.__max_cookie_age = config.get_as_long_with_default('options.max_cookie_age', self.__max_cookie_age)

    def set_references(self, references: IReferences):
        super().set_references(references)
        self._accounts_service = self._dependency_resolver.get_one_required('accounts-service')
        self._passwords_service = self._dependency_resolver.get_one_required('passwords-service') 
        self._sessions_service = self._dependency_resolver.get_one_required("sessions-service")
        self._roles_service = self._dependency_resolver.get_one_required("roles-service")
        self._settings_service = self._dependency_resolver.get_one_required('settings-service')


    def load_session(self):
        context = Context.from_trace_id(self._get_trace_id())
        self._logger.info(context, "----------load_session() invoked")
        
        # parse headers first, and if nothing in headers get cookie
        session_id = bottle.request.headers.get('x-session-id')
            
        if session_id:
            try:
                session = self._sessions_service.get_session_by_id('facade', session_id)
                if session is None:
                    raise UnauthorizedException(
                        'facade',
                        'SESSION_NOT_FOUND',
                        'Session invalid or already expired.'
                    ).with_details('session_id', session_id).with_status(440)
                
                bottle.request.user_id = session.user_id
                bottle.request.user_name = session.user_name
                bottle.request.user = session.user
                bottle.request.session_id = session.id
                
            except Exception as err:
                return self._send_error(err)
            
    def get_sessions(self):
        context = Context.from_trace_id(self._get_trace_id())
        self._logger.info(context, "----------get_sessions() invoked")

        filter_params = self._get_filter_params()
        paging_params = self._get_paging_params()
        try:
            res = self._sessions_service.get_sessions(context, filter_params, paging_params)
            return self._send_result(res)
        except Exception as err:
            return self._send_error(err)

    def get_session_by_id(self, session_id):
        context = Context.from_trace_id(self._get_trace_id())
        self._logger.info(context, "----------get_session_by_id() invoked")

        try:
            res = self._sessions_service.get_session_by_id(context, session_id)
            return self._send_result(res)
        except Exception as err:
            return self._send_error(err)


    def open_session(self, account: AccountV1, roles: List[str], ):
        context = Context.from_trace_id(self._get_trace_id())
        self._logger.info(context, "----------open_session() invoked")

        try:
            session: SessionV1 = None
            # sites: List[SiteV1] = None
            passwordInfo: UserPasswordInfoV1 = None
            settings: ConfigParams = None

            # Retrieve sites for user

            site_roles = [] if not roles else list(filter(lambda x: x.find(':') > 0, roles))
            # site_ids = [] if not site_roles else list(map(lambda x: x[0:x.find(':')] if x.find(':') >= 0 else x, site_roles))

            # if len(site_ids) > 0:
            #     filter_params = FilterParams.from_tuples('ids', site_ids)
            #     page = self.__sites_client.get_sites(None, filter_params, None)
            #     sites = [] if page is None else page.data
            # else:
            #     sites = []

            password_info = self._passwords_service.get_password_info(context, account.id)

            settings = self._settings_service.get_section_by_id(context, account.id)

            # Open a new user session
            user = SessionUserV1(
                id=account.id,
                name=account.name,
                login=account.login,
                create_time=account.create_time,
                time_zone=account.time_zone,
                language=account.language,
                theme=account.theme,
                roles=roles,
                sites=[],
                # sites=list(map(lambda x: {'id': x.id, 'name': x.name}, sites)),
                settings=settings,
                change_pwd_time=None if password_info is None else password_info.change_time,
                custom_hdr=account.custom_hdr,
                custom_dat=account.custom_dat
            )

            address = HttpRequestDetector.detect_address(bottle.request)
            client = HttpRequestDetector.detect_browser(bottle.request)
            platform = HttpRequestDetector.detect_platform(bottle.request)

            session = self._sessions_service.open_session(context, account.id, account.name, address, client, user.to_dict(), None)
            return JsonConverter.to_json(session)
        except Exception as err:
            return self._send_error(err)

    def store_session_data(self, session_id):
        context = Context.from_trace_id(self._get_trace_id())
        self._logger.info(context, "----------store_session_data() invoked")

        data = bottle.request.json or {}
        try:
            res = self._sessions_service.store_session_data(context, session_id, data)
            return self._send_result(res)
        except Exception as err:
            return self._send_error(err)

    def update_session_user(self, session_id):
        context = Context.from_trace_id(self._get_trace_id())
        self._logger.info(context, "----------update_session_user() invoked")

        data = bottle.request.json or {}
        try:
            res = self._sessions_service.update_session_user(context, session_id, data)
            return self._send_result(res)
        except Exception as err:
            return self._send_error(err)

    def close_session(self, session_id):
        context = Context.from_trace_id(self._get_trace_id())
        self._logger.info(context, "----------close_session() invoked")

        try:
            res = self._sessions_service.close_session(context, session_id)
            return self._send_result(res)
        except Exception as err:
            return self._send_error(err)

    def delete_session_by_id(self, session_id):
        context = Context.from_trace_id(self._get_trace_id())
        self._logger.info(context, "----------delete_session_by_id() invoked")

        try:
            res = self._sessions_service.delete_session_by_id(context, session_id)
            return self._send_result(res)
        except Exception as err:
            return self._send_error(err)
        
    def signup(self):
        context = Context.from_trace_id(self._get_trace_id())
        self._logger.info(context, "----------signup() invoked")

        try:
            signup_data = bottle.request.json if isinstance(bottle.request.json, dict) else JsonConverter.from_json(
                TypeCode.Map, bottle.request.json)
            account: AccountV1 = None
            invited: bool = False
            roles: List[str] = []

            # Validate password first
            # Todo: complete implementation after validate password is added

            # Create account
            new_account = AccountV1(
                None,
                login=signup_data.get('login') or signup_data.get('email'),
                name=signup_data.get('name'),
                language=signup_data.get('language'),
                theme=signup_data.get('theme'),
                time_zone=signup_data.get('time_zone')
            )

            account = self._accounts_service.create_account(context, new_account)

            # Create password for the account
            password = signup_data.get('password')

            self._passwords_service.set_password(context, account.id, password)

            # Activate all pending invitations
            email = signup_data.get('email')

            # invitations = self.__invitations_client.activate_invitations(context, email, account.id)
            # if invitations:
            #     # Calculate user roles from activated invitations
            #     for invitation in invitations:
            #         # Was user invited with the same email?
            #         invited = invited or email == invitation.invitee_email

            #         if invitation.site_id:
            #             invitation.role = invitation.role or 'user'
            #             role = invitation.site_id + ':' + invitation.role
            #             roles.append(role)

            # # Create email settings for the account
            # new_email_settings = EmailSettingsV1(
            #     id=account.id,
            #     name=account.name,
            #     email=email,
            #     language=account.language
            # )

            # if self.__email_settings_client is not None:
            #     if invited:
            #         self.__email_settings_client.set_verified_settings(context, new_email_settings)
            #     else:
            #         self.__email_settings_client.set_settings(context, new_email_settings)

            return self.open_session(account, roles)
        except Exception as err:
            return self._send_error(err)

    def signup_validate(self):
        context = Context.from_trace_id(self._get_trace_id())
        self._logger.info(context, "----------signup_validate() invoked")

        login = dict(bottle.request.query.decode()).get('login')

        if login:
            try:
                account = self._accounts_service.get_account_by_id_or_login(context, login)
                if account:
                    raise BadRequestException(
                        None, 'LOGIN_ALREADY_USED',
                        'Login ' + login + ' already being used'
                    ).with_details('login', login)

                return bottle.HTTPResponse(status=204)

            except Exception as err:
                return self._send_error(err)
        else:
            return bottle.HTTPResponse(status=204)

    def signin(self):
        context = Context.from_trace_id(self._get_trace_id())
        self._logger.info(context, "----------signin() invoked")

        json_data = bottle.request.json if isinstance(bottle.request.json, dict) else JsonConverter.from_json(
            TypeCode.Map, bottle.request.json)

        login = json_data.get('login')
        password = json_data.get('password')

        account: AccountV1 = None
        roles: List[str] = []

        # Find user account
        try:
            account = self._accounts_service.get_account_by_id_or_login(context, login)

            if account is None:
                raise BadRequestException(
                    None,
                    'WRONG_LOGIN',
                    'Account ' + login + ' was not found'
                ).with_details('login', login)

            # Authenticate user
            result = self._passwords_service.authenticate(context, account.id, password)
            # wrong password error is UNKNOWN when use http client
            if result is False:
                raise BadRequestException(
                    None,
                    'WRONG_PASSWORD',
                    'Wrong password for account ' + login
                ).with_details('login', login)

            # Retrieve user roles
            if self._roles_service:
                roles = self._roles_service.get_roles_by_id(context, account.id)
            else:
                roles = []

            return self.open_session(account, roles)
        except Exception as err:
            return self._send_error(err)
    
    def close_expired_sessions(self):
        context = Context.from_trace_id(self._get_trace_id())
        self._logger.info(context, "----------close_expired_sessions() invoked")

        try:
            self._sessions_service.close_expired_sessions(context)
            return self._send_empty_result()
        except Exception as err:
            return self._send_error(err)
        
    def restore_session(self):
        context = Context.from_trace_id(self._get_trace_id())
        self._logger.info(context, "----------restore_session() invoked")
        try:
            session_id = bottle.request.headers.get('x-session-id')

            session = self._sessions_service.get_session_by_id(context, session_id)

            # If session closed then return null
            if session and not session.active:
                session = None

            if session:
                return JsonConverter.to_json(session)
            else:
                return bottle.HTTPResponse(status=204)
        except Exception as err:
            return self._send_error(err)
        
    def signout(self):
        context = Context.from_trace_id(self._get_trace_id())
        self._logger.info(context, "----------signout() invoked")
        if hasattr(bottle.request, 'session_id'):
            try:
                self._sessions_service.close_session(context, bottle.request.session_id)
                return bottle.HTTPResponse(status=204)
            except Exception as err:
                self._send_error(err)

        return bottle.HTTPResponse(status=204)

    def get_user_sessions(self, user_id):
        context = Context.from_trace_id(self._get_trace_id())
        self._logger.info(context, "----------get_user_sessions() invoked")

        filter_params = self._get_filter_params()
        paging = self._get_paging_params()

        filter_params.set_as_object('user_id', user_id)

        sessions = self._sessions_service.get_sessions(context, filter_params, paging)
        return self._send_result(sessions.to_json())
        
    def get_current_session(self):
        context = Context.from_trace_id(self._get_trace_id())
        self._logger.info(context, "----------get_current_session() invoked")

        # parse headers first, and if nothing in headers get cookie
        session_id = bottle.request.headers.get('x-session-id')

        session = self._sessions_service.get_session_by_id(context, session_id)
        return self._send_result(session)

    def register_routes(self, controller: RestController, auth: AuthorizerV1):
        controller.register_route_with_auth('post', '/users/signup', None, auth.anybody(), lambda: self.signup())
        
        controller.register_route_with_auth('get', '/users/signup/validate', None, auth.anybody(), lambda: self.signup_validate())
        
        controller.register_route_with_auth('post', '/users/signin', None, auth.anybody(), lambda: self.signin())
        
        controller.register_route_with_auth('post', '/users/signout', None, auth.anybody(),lambda: self.signout())
        
        controller.register_route_with_auth('get', '/users/sessions', None, auth.admin(), lambda: self.get_sessions())
        
        controller.register_route_with_auth('post', '/users/sessions/restore', None, auth.signed(), lambda: self.restore_session())
        
        controller.register_route_with_auth('get', '/users/sessions/current', None, auth.signed(), lambda: self.get_current_session())
        
        controller.register_route_with_auth('get', '/users/:user_id/sessions', None, auth.signed(), lambda user_id: self.get_user_sessions(user_id))
        
        controller.register_route_with_auth('del', '/users/:user_id/sessions/:session_id', None, auth.signed(), 
                                  lambda user_id, session_id: self.close_session(user_id, session_id))

