# app/utils/objectid.py
from bson import ObjectId
from typing import Optional

def to_object_id(id_str: str) -> Optional[ObjectId]:
    try:
        return ObjectId(id_str)
    except Exception:
        return None
