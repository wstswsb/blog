from bson import ObjectId
from .model import Model
from .token_pair import TokenPair


class User(Model):
    def __init__(self, id: ObjectId = None) -> None:
        self.id: ObjectId = id
        self.email: str = None
        self.password_hash: bytes = None
        self.first_name: str = None
        self.last_name: str = None
        self.tokens: list[TokenPair] = None

    def assign_request(self, args: dict) -> None:
        ...
        # Todo: define the fields to be used

    @staticmethod
    def from_request(args: dict) -> "User":
        user = User()
        user.email = args.get("email")
        user.password_hash = args.get("password_hash")
        user.first_name = args.get("first_name")
        user.last_name = args.get("last_name")
        return user
