from typing import Dict, Optional

from .base_object import BaseObject


class CodeBaseObject(BaseObject):
    def __init__(self, data: Dict[str, any]):
        super().__init__(data)
        self._title = data['title']
        self._str_code = data['strCode']

    @property
    def title(self) -> str:
        return self._title

    @property
    def str_code(self) -> Optional[str]:
        return self._str_code

