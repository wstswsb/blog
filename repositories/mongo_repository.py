from bson import ObjectId
import math
from models import Model, Page


class MongoRepository:
    def __init__(self, translator, collection):
        """Default repository for MongoDb

           Keyword arguments:
           translator -- an object that can convert a model to a document
                         and vice versa.
           collection -- an object for working with a database

        """

        self.translator = translator
        self.collection = collection

    def create(self, model: Model) -> ObjectId:
        return self.collection.insert_one(self.translator.to_document(model)) \
            .inserted_id

    def get_by_id(self, obj_id: ObjectId) -> Model:
        model = self.collection.find_one({"_id": obj_id})
        if not model:
            return None
        return self.translator.from_document(model)

    def delete(self, obj_id: ObjectId) -> None:
        self.collection.delete_one({"_id": obj_id})

    def update(self, model: Model) -> Model:
        self.collection.update_one(
            {"_id": model.id},
            {"$set": self.translator.to_document(model)})
        return model

    def get_one_by_field(self, field_name: str, value) -> Model:
        # Todo: Test it
        model = self.collection.find_one({field_name: value})
        if not model:
            return None
        return self.translator.from_document(model)

    def exists(self, obj_id: ObjectId) -> bool:
        return self.get_by_id(obj_id) is not None

    def documents_count(self) -> int:
        return self.collection.count_documents({})

    def get_number_of_pages(self, page_size: int) -> int:
        number_of_documents = self.collection.count_documents({})
        number_of_pages = math.ceil(number_of_documents / page_size)
        return number_of_pages if number_of_pages != 0 else 1
