# -*- coding: utf-8 -*-
import datetime

from pip_services4_components.context import Context
from pip_services4_data.query import FilterParams, PagingParams
from pip_services4_components.refer import References, Descriptor

from eic_aichat_users.activities.data import PartyActivityV1, ReferenceV1
from eic_aichat_users.activities.logic import ActivitiesService
from eic_aichat_users.activities.persistence import ActivitiesMemoryPersistence


class TestActivitiesService:
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

    def setup_method(self):
        self.persistence = ActivitiesMemoryPersistence()
        self.service = ActivitiesService()
        
        self.references = References.from_tuples(
            Descriptor('activities', 'persistence', 'memory', 'default', '1.0'), self.persistence,
            Descriptor('activities', 'service', 'default', 'default', '1.0'), self.service
        )

        self.service.set_references(self.references)
        self.service

    def test_get_activities(self):
        # Create activities
        self.service.log_activity(Context.from_trace_id('123'), self.activity1)
        self.service.log_activity(Context.from_trace_id('123'), self.activity2)
        self.service.log_activity(Context.from_trace_id('123'), self.activity3)

        # Get all activities
        page = self.service.get_activities(
            Context.from_trace_id('123'),
            FilterParams(),
            PagingParams()
        )
        assert len(page.data) == 3

        # Get activities by party id
        page = self.service.get_activities(
            Context.from_trace_id('123'),
            FilterParams.from_tuples('party_id', '1'),
            PagingParams()
        )
        assert len(page.data) == 2

        # Get activities by ref item id
        page = self.service.get_activities(
            Context.from_trace_id('123'),
            FilterParams.from_tuples('ref_item_id', '2'),
            PagingParams()
        )
        assert len(page.data) == 2

    def test_log_activity(self):
        # Log activity
        activity = self.service.log_activity(Context.from_trace_id('123'), self.activity1)
        assert activity is not None
        assert activity.id == self.activity1.id
        assert activity.type == self.activity1.type
        assert activity.party.id == self.activity1.party.id

        # Get activity by id
        page = self.service.get_activities(
            Context.from_trace_id('123'),
            FilterParams.from_tuples('id', activity.id),
            PagingParams()
        )
        assert len(page.data) == 1

    def test_batch_log_activities(self):
        # Batch log activities
        self.service.batch_log_activities(
            Context.from_trace_id('123'),
            [self.activity1, self.activity2]
        )

        # Get all activities
        page = self.service.get_activities(
            Context.from_trace_id('123'),
            FilterParams(),
            PagingParams()
        )
        assert len(page.data) == 2

    def test_delete_activities_by_filter(self):
        # Create activities
        self.service.log_activity(Context.from_trace_id('123'), self.activity1)
        self.service.log_activity(Context.from_trace_id('123'), self.activity2)
        self.service.log_activity(Context.from_trace_id('123'), self.activity3)

        # Delete activities by party id
        self.service.delete_activities_by_filter(
            Context.from_trace_id('123'),
            FilterParams.from_tuples('party_id', '1')
        )

        # Get remaining activities
        page = self.service.get_activities(
            Context.from_trace_id('123'),
            FilterParams(),
            PagingParams()
        )
        assert len(page.data) == 1
        assert page.data[0].id == self.activity3.id 