# -*- coding: utf-8 -*-
from pip_services4_commons.convert import TypeCode
from pip_services4_data.validate import ObjectSchema, MapSchema
from pip_services4_data.validate import ArraySchema

from .ReferenceV1Schema import ReferenceV1Schema


class PartyActivityV1Schema(ObjectSchema):
    """
    Schema for validating PartyActivityV1 objects
    """
    
    def __init__(self):
        super().__init__()
        
        self.with_optional_property('id', TypeCode.String)
        self.with_optional_property('time', TypeCode.DateTime)
        self.with_required_property('type', TypeCode.String)
        self.with_required_property('party', ReferenceV1Schema())
        self.with_optional_property('ref_item', ReferenceV1Schema())
        self.with_optional_property('ref_parents', ArraySchema(ReferenceV1Schema()))
        self.with_optional_property('ref_party', ReferenceV1Schema())
        self.with_optional_property('details', MapSchema(TypeCode.String, TypeCode.String)) 