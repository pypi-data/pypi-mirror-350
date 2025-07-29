from enum import Enum


__all__ = (
    'OrderingType',
)


class OrderingType(str, Enum):
    desc = 'desc'
    asc = 'asc'
