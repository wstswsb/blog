from validators import PresenceValidator


class TestPresenceValidator:

    def test_valid_key_not_in_args(self):
        key = "key"
        args = {"not_key": 123}
        validator = PresenceValidator(key=key)

        assert validator.valid(args) is False

    def test_valid_valid(self):
        key = "key"
        args = {key: "value"}
        validator = PresenceValidator(key=key)

        assert validator.valid(args) is True
