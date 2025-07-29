# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
import hashlib
import random
import string
from typing import Optional

from pip_services4_components.config import ConfigParams, IConfigurable
from pip_services4_components.refer import IReferenceable, IReferences, Descriptor
from pip_services4_observability.log import CompositeLogger
from pip_services4_data.keys import IdGenerator
from pip_services4_components.context import IContext
from pip_services4_commons.errors import BadRequestException, NotFoundException

from .ActivitiesConnector import ActivitiesConnector
from ...activities.logic import ActivitiesService

from ..persistence.IPasswordsPersistence import IPasswordsPersistence

from ..data.version1.UserPasswordV1 import UserPasswordV1
from ..data.version1.UserPasswordInfoV1 import UserPasswordInfoV1

from .IPasswordsService import IPasswordsService

# TODO
class DummyMessageDistributionClient:
    def sendPasswordChangedEmail(self, context, user_id):
        pass

    def sendAccountLockedEmail(self, context, user_id):
        pass

    def sendRecoverPasswordEmail(self, context, user_id):
        pass

class PasswordsService(IConfigurable, IReferenceable, IPasswordsService):
    def __init__(self):
        self._persistence: IPasswordsPersistence = None
        self._logger: CompositeLogger = CompositeLogger()
        self._activities_connector: ActivitiesConnector = None
        self._activities_service: ActivitiesService = None
        self._message_distribution_client = DummyMessageDistributionClient()

        self._lock_timeout = 1800000 # 30 mins
        self._attempt_timeout = 60000 # 1 min
        self._attempt_count = 4 # 4 times
        self._rec_expire_timeout = 24 * 3600000 # 24 hours
        self._lock_enabled = False
        self._magic_code = None
        self._code_length = 9 # Generated code length

        self._max_password_len = 20
        self._min_password_len = 5

        self._old_passwords_check = False
        self._old_passwords_count = 6


    def configure(self, config: ConfigParams):
        self._lock_timeout = config.get_as_integer_with_default('options.lock_timeout', self._lock_timeout)
        self._attempt_timeout = config.get_as_integer_with_default('options.attempt_timeout', self._attempt_timeout)
        self._attempt_count = config.get_as_integer_with_default('options.attempt_count', self._attempt_count)
        self._rec_expire_timeout = config.get_as_integer_with_default('options.rec_expire_timeout', self._rec_expire_timeout)
        self._lock_enabled = config.get_as_boolean_with_default('options.lock_enabled', self._lock_enabled)
        self._magic_code = config.get_as_string_with_default('options.magic_code', self._magic_code)
        self._code_length = max(3, min(9, config.get_as_integer_with_default('options.code_length', self._code_length)))

        self._max_password_len = config.get_as_integer_with_default('options.max_password_len', self._max_password_len)
        self._min_password_len = config.get_as_integer_with_default('options.min_password_len', self._min_password_len)

        self._old_passwords_check = config.get_as_boolean_with_default('options.old_passwords_check', self._old_passwords_check)
        self._old_passwords_count = config.get_as_integer_with_default('options.old_passwords_count', self._old_passwords_count)

    def set_references(self, references: IReferences):
        self._logger.set_references(references)
        self._persistence = references.get_one_required(Descriptor('aichatusers-passwords', 'persistence', '*', '*', '1.0'))
        
        self._activities_service = references.get_one_optional(Descriptor('aichatusers-activities', 'service', '*', '*', '1.0'))
        if self._activities_service is not None:
            self._activities_service.set_references(references)
        
        self._activities_connector = ActivitiesConnector(self._logger, self._activities_service)

    def _generate_verification_code(self) -> str:
        return IdGenerator.next_short()[:self._code_length]
    
    def _hash_password(self, password: str) -> str:
        if not password:
            return None
        return hashlib.sha256(password.encode()).hexdigest()
    
    def _add_old_password(self, password_obj: UserPasswordV1, old_password: str) -> UserPasswordV1:
        if not password_obj.custom_dat:
            password_obj.custom_dat = {'old_passwords': []}
        old_pwds = password_obj.custom_dat.get('old_passwords', [])
        if len(old_pwds) >= self._old_passwords_count:
            old_pwds = old_pwds[1:]
        old_pwds.append(old_password)
        password_obj.custom_dat['old_passwords'] = old_pwds
        return password_obj
    
    def _generate_random_password(self, length: Optional[int] = None) -> str:
        length = length or random.randint(12, 16)
        return ''.join(random.choices(string.printable[33:127], k=length))
    
    def _verify_password(self, context: Optional[IContext], password: str, user_id: Optional[str] = None) -> None:
        if not password:
            raise BadRequestException(
                context,
                'NO_PASSWORD',
                'Missing user password'
            )

        if len(password) < self._min_password_len or len(password) > self._max_password_len:
            raise BadRequestException(
                context,
                'BAD_PASSWORD',
                f'User password should be {self._min_password_len} to {self._max_password_len} symbols long'
            )

        if user_id and self._old_passwords_check:
            old_password_err = None
            try:
                user_password = self._read_user_password(context, user_id)
            except NotFoundException:
                return
            except Exception as err:
                raise err

            if user_password:
                if not user_password.custom_dat:
                    user_password.custom_dat = {'old_passwords': []}
                old_passwords = user_password.custom_dat.get('old_passwords', [])

                hashed = self._hash_password(password)
                for old_pass in old_passwords:
                    if old_pass == hashed:
                        old_password_err = BadRequestException(
                            context,
                            'OLD_PASSWORD',
                            'Old password used'
                        )

            if old_password_err:
                raise old_password_err
            
    def validate_password(self, context: Optional[IContext], password: str) -> None:
        self._verify_password(context, password, None)

    def _read_user_password(self, context: Optional[IContext], user_id: str) -> UserPasswordV1:
        item = self._persistence.get_one_by_id(context, user_id)

        if item is None:
            raise NotFoundException(
                context,
                'USER_NOT_FOUND',
                f'User {user_id} was not found'
            ).with_details('user_id', user_id)

        return item

    def validate_password_for_user(self, context: Optional[IContext], user_id: str, password: str) -> None:
        self._verify_password(context, password, user_id)

    def get_password_info(self, context: Optional[IContext], user_id: str) -> UserPasswordInfoV1:
        data = self._persistence.get_one_by_id(context, user_id)

        if data is not None:
            return UserPasswordInfoV1(
                id=data.id,
                change_time=data.change_time,
                locked=data.locked,
                lock_time=data.lock_time
            )
        return None

    def set_password(self, context: Optional[IContext], user_id: str, password: str) -> None:
        self._verify_password(context, password, user_id)

        userPassword = self._persistence.get_one_by_id(context, user_id)
        password = self._hash_password(password)

        if userPassword is not None:
            userPassword = self._add_old_password(userPassword, userPassword.password)
        else:
            userPassword = UserPasswordV1(user_id, password)

        self._persistence.create(context, userPassword)

    def set_temp_password(self, context: Optional[IContext], user_id: str) -> str:
        password = self._generate_random_password()
        passwordHash = self._hash_password(password)

        userPassword = UserPasswordV1(user_id, passwordHash)
        userPassword.change_time = datetime.now()

        self._persistence.create(context, userPassword)
        return password

    def delete_password(self, context: Optional[IContext], user_id: str) -> None:
        self._persistence.delete_by_id(context, user_id)

    def authenticate(self, context: Optional[IContext], user_id: str, password: str) -> bool:
        hashed_password = self._hash_password(password)
        current_time = datetime.utcnow()

        user_password = self._read_user_password(context, user_id)

        password_match = user_password.password == hashed_password
        last_failure_timeout = (
            (current_time - user_password.fail_time).total_seconds() * 1000
            if user_password.fail_time else None
        )

        if not self._lock_enabled and password_match:
            user_password.locked = False
        else:
            if password_match and user_password.locked and last_failure_timeout and last_failure_timeout > self._lock_timeout:
                user_password.locked = False
            elif user_password.locked:
                raise BadRequestException(
                    context,
                    'ACCOUNT_LOCKED',
                    f'Account for user {user_id} is locked'
                ).with_details('user_id', user_id)

            if not password_match:
                if last_failure_timeout is None or last_failure_timeout < self._attempt_timeout:
                    user_password.fail_count = (user_password.fail_count or 0) + 1

                user_password.fail_time = current_time

                try:
                    self._persistence.update(context, user_password)
                except Exception as err:
                    self._logger.error(context, err, 'Failed to save user password')

                if user_password.fail_count >= self._attempt_count:
                    user_password.locked = True

                    self._message_distribution_client.sendAccountLockedEmail(context, user_id)

                    raise BadRequestException(
                        context,
                        'ACCOUNT_LOCKED',
                        f'Number of attempts exceeded. Account for user {user_id} was locked'
                    ).with_details('user_id', user_id)
                else:
                    raise BadRequestException(
                        context,
                        'WRONG_PASSWORD',
                        'Invalid password'
                    ).with_details('user_id', user_id)

        user_password.fail_count = 0
        user_password.fail_time = None

        self._persistence.update(context, user_password)
        self._activities_connector.log_signin_activity(context, user_id)

        return True

    def change_password(self, context: Optional[IContext], user_id: str, old_password: str, new_password: str) -> None:
        
        self._verify_password(context, new_password, user_id)

        old_password_hashed = self._hash_password(old_password)
        new_password_hashed = self._hash_password(new_password)

        user_password = self._read_user_password(context, user_id)

        if user_password.password != old_password_hashed:
            raise BadRequestException(
                context,
                'WRONG_PASSWORD',
                'Invalid password'
            ).with_details('user_id', user_id)

        if old_password_hashed == new_password_hashed:
            raise BadRequestException(
                context,
                'PASSWORD_NOT_CHANGED',
                'Old and new passwords are identical'
            ).with_details('user_id', user_id)

        user_password = self._add_old_password(user_password, old_password_hashed)
        user_password.password = new_password_hashed
        user_password.rec_code = None
        user_password.rec_expire_time = None
        user_password.locked = False
        user_password.change_time = None

        self._persistence.update(context, user_password)

        self._activities_connector.log_password_changed_activity(context, user_id)
        self._message_distribution_client.sendPasswordChangedEmail(context, user_id)

    def validate_code(self, context: Optional[IContext], user_id: str, code: str) -> bool:
        data = self._read_user_password(context, user_id)
        if data is None:
            return False

        now = datetime.utcnow()
        valid = (
            code == self._magic_code or
            (data.rec_code == code and data.rec_expire_time and data.rec_expire_time > now)
        )
        return valid

    def reset_password(self, context: Optional[IContext], user_id: str, code: str, password: str) -> None:
        self._verify_password(context, password, user_id)

        password_hashed = self._hash_password(password)

        user_password = self._read_user_password(context, user_id)

        if user_password.rec_code != code and code != self._magic_code:
            raise BadRequestException(
                context,
                'WRONG_CODE',
                f'Invalid password recovery code {code}'
            ).with_details('user_id', user_id)

        if (not user_password.rec_expire_time or user_password.rec_expire_time <= datetime.utcnow()) and code != self._magic_code:
            raise BadRequestException(
                context,
                'CODE_EXPIRED',
                f'Password recovery code {code} expired'
            ).with_details('user_id', user_id)

        user_password.password = password_hashed
        user_password.rec_code = None
        user_password.rec_expire_time = None
        user_password.locked = False
        user_password.change_time = None 

        self._persistence.update(context, user_password)

        self._activities_connector.log_password_changed_activity(context, user_id)
        self._message_distribution_client.sendPasswordChangedEmail(context, user_id)

    def recover_password(self, context: Optional[IContext], user_id: str) -> None:
        user_password = self._persistence.get_one_by_id(context, user_id)
        if user_password is None:
            raise NotFoundException(context, 'USER_NOT_FOUND', f'User {user_id} was not found')

        current_time = datetime.utcnow()
        expire_time = current_time + timedelta(milliseconds=self._rec_expire_timeout)

        user_password.rec_code = self._generate_verification_code()
        user_password.rec_expire_time = expire_time

        self._persistence.update(context, user_password)

        self._activities_connector.log_password_recovered_activity(context, user_id)
        self._message_distribution_client.sendRecoverPasswordEmail(context, user_id)
        # TODO:
        return "a message with a recovery link will be sent to the post office in the future...."
    


