# -*- coding: utf-8 -*-
from datetime import datetime
from pip_services4_data.query import FilterParams, PagingParams
from pip_services4_commons.data import AnyValueMap

from eic_aichat_users.sessions.data.SessionV1 import SessionV1
from eic_aichat_users.sessions.persistence.ISessionsPersistence import ISessionsPersistence


SESSION1 = SessionV1(user_id='1', user_name='User 1')
SESSION2 = SessionV1(user_id='2', user_name='User 2')


class SessionsPersistenceFixture:
    def __init__(self, persistence: ISessionsPersistence):
        assert persistence is not None
        self._persistence = persistence

    def test_crud_operations(self):
        # Create the first session
        session1 = self._persistence.create(None, SESSION1)
        assert session1 is not None
        assert session1.id is not None
        assert session1.open_time is not None
        assert session1.request_time is not None
        assert session1.user_id == SESSION1.user_id

        # Create the second session
        session2 = self._persistence.create(None, SESSION2)
        assert session2 is not None
        assert session2.id is not None
        assert session2.open_time is not None
        assert session2.request_time is not None
        assert session2.user_id == SESSION2.user_id

        # Partially update session
        updated = self._persistence.update_partially(
            None,
            session1.id,
            AnyValueMap.from_tuples("data", "123")
        )
        assert updated is not None
        assert updated.id == session1.id
        assert updated.data == "123"

        # Get session by filter
        page = self._persistence.get_page_by_filter(
            None,
            FilterParams.from_tuples("user_id", "1"),
            PagingParams()
        )
        assert page is not None
        assert len(page.data) == 1

    def test_close_expired(self):
        self._persistence.close_expired(None, datetime.utcnow())
