from typing import Dict, Callable, Optional

from .content_loader import none_loader, scalar_loader, json_loader
from ..enum import DatasetTypeEnum

content_loder_dict: Dict[str, Callable[[Optional[str]], any]] = {
    DatasetTypeEnum.NONE: none_loader,
    DatasetTypeEnum.SCALAR: scalar_loader,
    DatasetTypeEnum.JSON: json_loader
}