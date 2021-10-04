from bson import ObjectId
from .mongo_repository import MongoRepository
from models import User


class UserRepository(MongoRepository):

    def create(self, model: User) -> ObjectId:
        if self.exists_email(model.email):
            return None
        return super().create(model)

    def exists_email(self, email: str) -> bool:
        return self.collection.find_one({"email": email}) is not None

    def password_hash_verification(
            self,
            email: str,
            password_hash: bytes) -> bool:
        doc = self.collection.find_one({"email": email})
        return password_hash == doc["password_hash"]
