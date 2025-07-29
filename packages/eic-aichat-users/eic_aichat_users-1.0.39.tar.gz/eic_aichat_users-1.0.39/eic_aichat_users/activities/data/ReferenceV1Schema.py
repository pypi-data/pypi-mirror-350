# -*- coding: utf-8 -*-
from pip_services4_commons.convert import TypeCode
from pip_services4_data.validate import ObjectSchema


class ReferenceV1Schema(ObjectSchema):
    """
    Schema for validating ReferenceV1 objects
    """
    
    def __init__(self):
        super().__init__()
        
        self.with_required_property('id', TypeCode.String)
        self.with_required_property('type', TypeCode.String)
        self.with_optional_property('name', TypeCode.String) 