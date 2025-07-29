# -*- coding: utf-8 -*-
from pip_services4_data.validate import ObjectSchema
from pip_services4_commons.convert import TypeCode


class SessionV1Schema(ObjectSchema):
    def __init__(self):
        super().__init__()

        self.with_optional_property('id', TypeCode.String)
        self.with_required_property('user_id', TypeCode.String)
        self.with_required_property('user_name', TypeCode.String)
        self.with_optional_property('active', TypeCode.Boolean)
        self.with_optional_property('open_time', None)
        self.with_optional_property('close_time', None)
        self.with_optional_property('request_time', None)
        self.with_optional_property('address', TypeCode.String)
        self.with_optional_property('client', TypeCode.String)
        self.with_optional_property('user', None)
        self.with_optional_property('data', None)
