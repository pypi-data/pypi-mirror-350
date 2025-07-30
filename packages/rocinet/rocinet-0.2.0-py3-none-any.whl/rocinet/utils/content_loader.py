from json import loads
from typing import Optional


def none_loader(input_value: Optional[str]) -> None:
    return None


def scalar_loader(input_value: Optional[str]) -> Optional[str]:
    return input_value


def json_loader(input_value: Optional[str]) -> Optional[dict]:
    return loads(input_value) if input_value else None
