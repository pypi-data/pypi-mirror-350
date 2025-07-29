# -*- coding: utf-8 -*-
from pip_services4_data.validate import ObjectSchema
from pip_services4_commons.convert import TypeCode


class SettingsSectionV1Schema(ObjectSchema):
    def __init__(self):
        super().__init__()
        self.with_required_property('id', TypeCode.String)
        self.with_optional_property('parameters', TypeCode.Map)
        self.with_optional_property('update_time', TypeCode.DateTime)
