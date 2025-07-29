import re
from typing import TypeVar

T = TypeVar("T")


def is_valid_resource_name(name: str):
    return re.match(r"^[a-z0-9-]+$", name)


def make_valid_resource_name(name: str):
    return re.sub(r"[^a-z0-9-]", "-", name)
