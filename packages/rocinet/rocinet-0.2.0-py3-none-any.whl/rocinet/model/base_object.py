from datetime import datetime
from json import loads
from typing import Dict, Optional


class BaseObject:
    def __init__(self, data: Dict[str, any]):
        self._id = data['id']
        self._active = data['active']
        self._valid = data['valid']
        self._create_time = datetime.fromisoformat(data['createTime'])

    @property
    def id(self) -> int:
        return self._id

    @property
    def active(self) -> bool:
        return self._active

    @property
    def valid(self) -> bool:
        return self._valid

    @property
    def create_time(self) -> datetime:
        return self._create_time
