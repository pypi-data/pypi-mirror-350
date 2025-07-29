# -*- coding: utf-8 -*-
from typing import Optional, List

from pip_services4_commons.convert import TypeCode
from pip_services4_data.validate import ObjectSchema, FilterParamsSchema, PagingParamsSchema
from pip_services4_data.validate import ArraySchema
from pip_services4_rpc.commands import CommandSet, ICommand, Command

from ..data import PartyActivityV1Schema


class ActivitiesCommandSet(CommandSet):
    _controller = None

    def __init__(self, controller):
        super().__init__()
        self._controller = controller

        self.add_command(self._make_get_activities_command())
        self.add_command(self._make_log_activity_command())
        self.add_command(self._make_batch_log_activities_command())
        self.add_command(self._make_delete_activities_by_filter_command())

    def _make_get_activities_command(self) -> ICommand:
        return Command(
            'get_activities',
            ObjectSchema(True)
                .with_optional_property('filter', FilterParamsSchema())
                .with_optional_property('paging', PagingParamsSchema()),
            lambda context, args: self._controller.get_activities(
                context,
                args.get('filter'),
                args.get('paging')
            )
        )

    def _make_log_activity_command(self) -> ICommand:
        return Command(
            'log_activity',
            ObjectSchema(True)
                .with_required_property('activity', PartyActivityV1Schema()),
            lambda context, args: self._controller.log_activity(
                context,
                args.get('activity')
            )
        )

    def _make_batch_log_activities_command(self) -> ICommand:
        return Command(
            'batch_log_activities',
            ObjectSchema(True)
                .with_required_property('activities', ArraySchema(PartyActivityV1Schema())),
            lambda context, args: self._controller.batch_log_activities(
                context,
                args.get('activities')
            )
        )

    def _make_delete_activities_by_filter_command(self) -> ICommand:
        return Command(
            'delete_activities_by_filter',
            ObjectSchema(True)
                .with_optional_property('filter', FilterParamsSchema()),
            lambda context, args: self._controller.delete_activities_by_filter(
                context,
                args.get('filter')
            )
        ) 