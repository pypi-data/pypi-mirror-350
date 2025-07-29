# -*- coding: utf-8 -*-

from pip_services4_observability.log import ILogger
from ...activities.data import PartyActivityV1, ReferenceV1
from ...activities.logic import IActivitiesService
from ..data.version1.PasswordActivityTypeV1 import PasswordActivityTypeV1


class ActivitiesConnector:
    def __init__(self, logger: ILogger, activities_service: IActivitiesService):
        self._logger = logger
        self._activities_service = activities_service

        if self._activities_service is None:
            self._logger.warn(None, 'Activities service was not found. Logging password activities is disabled')

    def log_activity(self, correlation_id: str, user_id: str, activity_type: str):
        if self._activities_service is None:
            return

        party = ReferenceV1(user_id, 'account', None)
        activity = PartyActivityV1(None, None, activity_type, party)

        try:
            self._activities_service.log_activity(correlation_id, activity)
        except Exception as err:
            self._logger.error(correlation_id, err, 'Failed to log user activity')

    def log_signin_activity(self, correlation_id: str, user_id: str):
        self.log_activity(correlation_id, user_id, PasswordActivityTypeV1.Signin)

    def log_password_recovered_activity(self, correlation_id: str, user_id: str):
        self.log_activity(correlation_id, user_id, PasswordActivityTypeV1.PasswordRecovered)

    def log_password_changed_activity(self, correlation_id: str, user_id: str):
        self.log_activity(correlation_id, user_id, PasswordActivityTypeV1.PasswordChanged)
