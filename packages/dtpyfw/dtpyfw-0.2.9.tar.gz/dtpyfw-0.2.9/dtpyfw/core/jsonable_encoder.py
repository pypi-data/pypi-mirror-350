import json
from typing import Any


__all__ = (
    'jsonable_encoder',
)


def jsonable_encoder(data: Any):
    return json.loads(json.dumps(data, default=str))
