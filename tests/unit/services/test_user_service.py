from exceptions.conflict import Conflict
import bcrypt
import pytest
from bson import ObjectId
from mock import Mock
from services import UserService
from models import User
from exceptions import Conflict


class TestUserService:

    def setup(self):
        self.repository = Mock()
        self.create_validate_service = Mock()
        self.user_service = UserService(
            repository=self.repository,
            create_validate_service=self.create_validate_service
        )

    def test_add_password_hash(self):
        args = {"password": "password"}
        salt = bcrypt.gensalt()
        self.user_service._gensalt = Mock()
        self.user_service._gensalt.return_value = salt

        self.user_service._add_password_hash(args)

        assert isinstance(args, dict)
        assert "password_hash" in args
        assert bcrypt.hashpw(
            args["password"].encode(), salt=salt) == args["password_hash"]

    def test_create_new_email(self):
        args = {
            "email": "vasya@gmail.com",
            "password": "password",
            "first_name": "first_name",
            "last_name": "last_name"
        }
        expected_id = ObjectId()
        self.repository.create.return_value = expected_id
        self.create_validate_service.validate.return_value = True

        result = self.user_service.create(args)

        assert isinstance(result, User)
        assert result.id == expected_id
        assert result.email == args["email"]
        assert result.first_name == args["first_name"]
        assert result.last_name == args["last_name"]
        self.create_validate_service.validate.assert_called_once_with(args)

    def test_create_exists_email(self):
        args = {
            "email": "vasya@gmail.com",
            "password": "password",
            "first_name": "first_name",
            "last_name": "last_name"
        }
        self.repository.create.return_value = None
        with pytest.raises(Conflict):
            self.user_service.create(args)
        self.create_validate_service.validate.assert_called_once_with(args)
