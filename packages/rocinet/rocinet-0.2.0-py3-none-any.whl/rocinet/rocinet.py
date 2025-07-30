from datetime import datetime
from typing import Union, Generator, Optional, Dict, Callable
from urllib.parse import quote

import requests

from .model import DataItem, Dataset, DatasetType
from .utils import content_loder_dict


class Rocinet:
    def __init__(self, access_token: str, list_size: int = 1000):
        self._access_token = access_token
        self._list_size = list_size
        self._dataset_types_str_dict: Dict[str, DatasetType] = {}
        self._dataset_types_int_dict: Dict[int, DatasetType] = {}
        self._dataset_str_dict: Dict[str, Dataset] = {}
        self._dataset_int_dict: Dict[int, Dataset] = {}

    def get_data_items(self, dataset: Union[str, int, Dataset], content_update_after: Optional[datetime] = None, content_update_before: Optional[datetime] = None) -> Generator[DataItem, None, None]:
        dataset = dataset if isinstance(dataset, Dataset) else self.get_dataset(dataset)
        loader = self._get_content_loader(dataset)

        filter_str = '&contentUpdateTime[>%3D]={}'.format(quote(content_update_after.isoformat())) if content_update_after is not None else ''
        filter_str += '&contentUpdateTime[<]={}'.format(quote(content_update_before.isoformat())) if content_update_before is not None else ''
        offset = 0
        stop = False
        while not stop:
            url = 'https://api.rocinet.com/datasets/{}/data_items?limit={}&offset={}&sort=createTime%2B{}'\
                .format(dataset.id, self._list_size, offset, filter_str)
            response = requests.get(url, headers=self._get_headers())
            response.raise_for_status()
            items = response.json().get('items')
            for item in items:
                yield DataItem(item, loader)
            offset += self._list_size
            stop = len(items) < self._list_size

    def get_dataset_type(self, unique: Union[str, int]) -> DatasetType:
        if not self._dataset_types_str_dict:
            self._load_dataset_types()
        if isinstance(unique, str):
            return self._dataset_types_str_dict[unique]
        else:
            return self._dataset_types_int_dict[unique]

    def get_dataset(self, unique: Union[str, int], force_reload: bool = False) -> Dataset:
        if isinstance(unique, str):
            dataset = self._dataset_str_dict.get(unique)
        else:
            dataset = self._dataset_int_dict.get(unique)
        if dataset is None or force_reload:
            return self._load_dataset(unique)
        else:
            return dataset

    def _load_dataset(self, unique: Union[str, int]) -> Dataset:
        url = 'https://api.rocinet.com/datasets/{}'.format(unique)
        response = requests.get(url, headers=self._get_headers())
        response.raise_for_status()
        data = response.json()
        dataset = Dataset(data)
        self._dataset_str_dict[dataset.str_code] = dataset
        self._dataset_int_dict[dataset.id] = dataset
        return dataset

    def _load_dataset_types(self) -> None:
        url = 'https://api.rocinet.com/dataset_types?limit=9999'
        response = requests.get(url, headers=self._get_headers())
        response.raise_for_status()
        items = response.json().get('items')
        for item in items:
            dataset_type = DatasetType(item)
            self._dataset_types_str_dict[dataset_type.str_code] = dataset_type
            self._dataset_types_int_dict[dataset_type.id] = dataset_type

    def _get_headers(self) -> dict:
        return {
            'Authorization': 'Bearer {}'.format(self._access_token),
            'Accept': 'application/json'
        }

    def _get_content_loader(self, dataset: Dataset) -> Callable[[Optional[str]], any]:
        dataset_type = self.get_dataset_type(dataset.dataset_type_id)
        loader = content_loder_dict.get(dataset_type.str_code)
        if loader is None:
            raise ValueError(f"Unsupported dataset type: {dataset_type.str_code}")
        else:
            return loader
