from bson import ObjectId
from bson.errors import InvalidId


class Repository:
    def __init__(self, translator) -> None:
        self.translator = translator

    def is_valid_obj_id(self, obj_id: str) -> bool:
        valid = True
        try:
            obj_id = ObjectId(obj_id)
            return valid
        except InvalidId:
            return not valid
