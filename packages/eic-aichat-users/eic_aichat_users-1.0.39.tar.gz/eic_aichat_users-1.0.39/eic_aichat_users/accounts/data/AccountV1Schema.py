# -*- coding: utf-8 -*-
from pip_services4_commons.convert import TypeCode
from pip_services4_data.validate import ObjectSchema


class AccountV1Schema(ObjectSchema):
    def __init__(self):
        super().__init__()

        self.with_optional_property('id', TypeCode.String)
        self.with_required_property('login', TypeCode.String)
        self.with_required_property('name', TypeCode.String)
        self.with_optional_property('create_time', TypeCode.DateTime)
        self.with_optional_property('deleted', TypeCode.Boolean)
        self.with_optional_property('active', TypeCode.Boolean)
        self.with_optional_property('about', TypeCode.String)
        self.with_optional_property('time_zone', TypeCode.String)
        self.with_optional_property('language', TypeCode.String)
        self.with_optional_property('theme', TypeCode.String)
        self.with_optional_property('custom_hdr', None)
        self.with_optional_property('custom_dat', None)
