

class TypeValidator():
    def __init__(self, key: str, type_: type) -> None:
        self.key = key
        self.value_type = type_

    def valid(self, args: dict) -> bool:
        return isinstance(args.get(self.key), self.value_type)

    def error(self) -> str:
        return \
            f"Error in [{self.key}]. Given value doesn't instance " \
            f"of {self.value_type}"
