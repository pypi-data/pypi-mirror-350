from datetime import datetime, timedelta
from json import loads
from typing import Dict, Optional

from .code_base_object import CodeBaseObject


class Dataset(CodeBaseObject):
    def __init__(self, data: Dict[str, any]):
        super().__init__(data)
        self._item_auto_delete_interval = timedelta(seconds=data['itemAutoDeleteInterval']) if data['itemAutoDeleteInterval'] is not None else None
        self._item_auto_delete_cascade = data['itemAutoDeleteCascade']
        self._public = data['public']
        self._workspace_id = data['workspace']
        self._data_collection_id = data['dataCollection']
        self._dataset_type_id = data['datasetType']

    @property
    def item_auto_delete_interval(self) -> Optional[timedelta]:
        return self._item_auto_delete_interval

    @property
    def item_auto_delete_cascade(self) -> bool:
        return self._item_auto_delete_cascade

    @property
    def public(self) -> bool:
        return self._public

    @property
    def workspace_id(self) -> int:
        return self._workspace_id

    @property
    def data_collection_id(self) -> Optional[int]:
        return self._data_collection_id

    @property
    def dataset_type_id(self) -> int:
        return self._dataset_type_id
