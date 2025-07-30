import json
from .odm import BaseModel, ObjectId

class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        if isinstance(obj, BaseModel):
            return obj.model_dump()
        return super().default(obj)


def print_json(data, *, indent: int = 4):
    try:
        print(json.dumps(data, cls=EnhancedJSONEncoder, indent=indent, ensure_ascii=False))
    except Exception as e:
        print(f"[print_json] error: {e}")