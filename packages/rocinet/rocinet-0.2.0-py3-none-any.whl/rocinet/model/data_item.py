from datetime import datetime
from json import loads
from typing import Dict, Optional, Callable

from .base_object import BaseObject


class DataItem(BaseObject):
    def __init__(self, data: Dict[str, any], content_loader: Callable[[Optional[str]], any] = None):
        super().__init__(data)
        self._key = data['key']
        self._sync_id = data['syncId']
        self._search_value = data['searchValue']
        self._hash = data['hash']
        self._content = content_loader(data['content'])
        self._source_update_time = datetime.fromisoformat(data['sourceUpdateTime']) if data['sourceUpdateTime'] else None
        self._content_update_time = datetime.fromisoformat(data['contentUpdateTime'])
        self._dataset_id = data['dataset']
        self._execution_id = data['execution']
        self._depend_on_id = data['dependOn']

    @property
    def key(self) -> str:
        return self._key

    @property
    def sync_id(self) -> Optional[int]:
        return self._sync_id

    @property
    def search_value(self) -> Optional[str]:
        return self._search_value

    @property
    def hash(self) -> str:
        return self._hash

    @property
    def content(self) -> Optional[Dict[str, any]]:
        return self._content

    @property
    def source_update_time(self) -> Optional[datetime]:
        return self._source_update_time

    @property
    def content_update_time(self) -> datetime:
        return self._content_update_time

    @property
    def dataset_id(self) -> int:
        return self._dataset_id

    @property
    def execution_id(self) -> Optional[int]:
        return self._execution_id

    @property
    def depend_on_id(self) -> Optional[int]:
        return self._depend_on_id

