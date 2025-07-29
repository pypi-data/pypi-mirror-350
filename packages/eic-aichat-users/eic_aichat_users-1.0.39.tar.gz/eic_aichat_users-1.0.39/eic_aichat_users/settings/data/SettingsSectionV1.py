# -*- coding: utf-8 -*-
from datetime import datetime
from typing import Optional
from pip_services4_data.data import IStringIdentifiable
from pip_services4_components.config import ConfigParams


class SettingsSectionV1(IStringIdentifiable):
    def __init__(self, id: str = None, parameters: Optional[ConfigParams] = None):
        self.id = id
        self.parameters = ConfigParams.from_value(parameters or {})
        self.update_time = datetime.now()
