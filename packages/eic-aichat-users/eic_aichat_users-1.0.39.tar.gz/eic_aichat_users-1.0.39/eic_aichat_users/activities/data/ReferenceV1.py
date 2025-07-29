# -*- coding: utf-8 -*-
from typing import Optional


class ReferenceV1:
    """
    Reference object used to identify a related object.
    
    Attributes:
        id (str): Unique identifier of the referenced object
        type (str): Type of the referenced object
        name (str): Human-readable name of the referenced object
    """
    
    def __init__(self, id: str = None, type: str = None, name: Optional[str] = None):
        """
        Creates a new reference to an object
        
        Args:
            id: Unique identifier of the referenced object
            type: Type of the referenced object
            name: Human-readable name of the referenced object
        """
        self.id = id
        self.type = type
        self.name = name