# -*- coding: utf-8 -*-
import datetime

from pip_services4_components.context import Context
from pip_services4_data.query import FilterParams, PagingParams

from eic_aichat_users.activities.data import PartyActivityV1, ReferenceV1


class ActivitiesPersistenceFixture:
    _persistence = None

    def __init__(self, persistence):
        self._persistence = persistence

    def test_crud_operations(self):
        # Create activity
        activity = PartyActivityV1(
            id='1',
            time=datetime.datetime.now(),
            type='test',
            party=ReferenceV1(id='1', type='party'),
            ref_item=ReferenceV1(id='1', type='item'),
            ref_parents=[],
            ref_party=None,
            details={}
        )

        created_activity = self._persistence.create(Context.from_trace_id('123'), activity)
        assert created_activity is not None
        # assert created_activity.id == activity.id
        assert created_activity.type == activity.type
        assert created_activity.party.id == activity.party.id

        # Get activity by id
        result = self._persistence.get_one_by_id(Context.from_trace_id('123'), created_activity.id)
        assert result is not None
        assert result.id == activity.id
        assert result.type == activity.type
        assert result.party.id == activity.party.id

        # Delete activity
        self._persistence.delete_by_id(Context.from_trace_id('123'), created_activity.id)

        # Try to get deleted activity
        result = self._persistence.get_one_by_id(Context.from_trace_id('123'), created_activity.id)
        assert result is None

    def test_get_with_filter(self):
        # Create activities
        activity1 = PartyActivityV1(
            id='1',
            time=datetime.datetime.now(),
            type='test',
            party=ReferenceV1(id='1', type='party'),
            ref_item=ReferenceV1(id='1', type='item'),
            ref_parents=[],
            ref_party=None,
            details={}
        )
        activity2 = PartyActivityV1(
            id='2',
            time=datetime.datetime.now(),
            type='test',
            party=ReferenceV1(id='1', type='party'),
            ref_item=ReferenceV1(id='2', type='item'),
            ref_parents=[],
            ref_party=None,
            details={}
        )
        activity3 = PartyActivityV1(
            id='3',
            time=datetime.datetime.now(),
            type='test',
            party=ReferenceV1(id='2', type='party'),
            ref_item=ReferenceV1(id='2', type='item'),
            ref_parents=[],
            ref_party=None,
            details={}
        )

        self._persistence.create(Context.from_trace_id('123'), activity1)
        self._persistence.create(Context.from_trace_id('123'), activity2)
        self._persistence.create(Context.from_trace_id('123'), activity3)

        # Get with filters
        page = self._persistence.get_page_by_filter(
            Context.from_trace_id('123'),
            FilterParams.from_tuples('party_id', '1'),
            PagingParams()
        )
        assert len(page.data) == 2

        page = self._persistence.get_page_by_filter(
            Context.from_trace_id('123'),
            FilterParams.from_tuples('ref_item_id', '2'),
            PagingParams()
        )
        assert len(page.data) == 2

        page = self._persistence.get_page_by_filter(
            Context.from_trace_id('123'),
            FilterParams.from_tuples('type', 'test'),
            PagingParams()
        )
        assert len(page.data) == 3 