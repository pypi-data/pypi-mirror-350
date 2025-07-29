# -*- coding: utf-8 -*-
from datetime import datetime
from typing import Dict, List, Any, Optional

from pip_services4_data.data import IStringIdentifiable
from pip_services4_commons.data import StringValueMap
from .ReferenceV1 import ReferenceV1


class PartyActivityV1(IStringIdentifiable):
    """
    Data object that represents a party activity.
    
    Attributes:
        id (str): Unique activity id
        time (datetime): Time when activity took place
        type (str): Activity type
        party (ReferenceV1): Reference to party who generated the activity
        ref_item (ReferenceV1): Reference to item that was subject of activity
        ref_parents (List[ReferenceV1]): References to parent items
        ref_party (ReferenceV1): Reference to party who was subject of activity
        details StringValueMap: Map with additional details
    """
    
    def __init__(self, id: str = None, time: datetime = None, type: str = None, 
                 party: ReferenceV1 = None, ref_item: ReferenceV1 = None, 
                 ref_parents: List[ReferenceV1] = None, ref_party: ReferenceV1 = None, 
                 details: StringValueMap = None):
        """
        Creates a new party activity
        
        Args:
            id: Unique activity id
            time: Time when activity took place
            type: Activity type
            party: Reference to party who generated the activity
            ref_item: Reference to item that was subject of activity
            ref_parents: References to parent items
            ref_party: Reference to party who was subject of activity
            details: Map with additional details
        """
        self.id = id
        self.time = time or datetime.now()
        self.type = type
        self.party = party
        self.ref_item = ref_item
        self.ref_parents = ref_parents or []
        self.ref_party = ref_party
        self.details = details or {}