from datetime import date, datetime, time
from typing import Any, Mapping

from bson import ObjectId


def parse_object_id(value: str) -> ObjectId | None:
    if not ObjectId.is_valid(value):
        return None

    return ObjectId(value)


def encode_mongo_update(data: Mapping[str, Any]) -> dict[str, Any]:
    return {
        key: (
            datetime.combine(value, time.min)
            if isinstance(value, date) and not isinstance(value, datetime)
            else value
        )
        for key, value in data.items()
    }
