import json
from typing import Any

def encode_json(value:Any) -> str | None:
    if value is None:
        return None
    return json.dumps(value,ensure_ascii=False)

def decode_json(value:str | None) -> Any:
    if value is None:
        return None
    try:
        return json.loads(value)
    except Exception:
        return value