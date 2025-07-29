import enum
import typing


class _QappEnumMeta(enum.EnumType):
    """
        Additional methods to be used for Enum Operations

        Ref - https://stackoverflow.com/a/62854511/13029007
    """

    # ------------------------------------------------------------

    def __contains__(cls, item: typing.Any) -> bool:
        """Check whether the Enum contains value"""

        try:
            cls(item)
        except ValueError:
            return False
        else:
            return True

    # ------------------------------------------------------------

    # def __getattribute__(cls, name):
    #     """
    #         Directly access the value of Enum instead of specifing .valie

    #         Example:
    #             class Test(Enum):
    #                 A = 'a'

    #             Old >>> Test.A.value -> 'a'
    #             New >>> Test.A -> 'a'

    #         Ref - https://stackoverflow.com/a/54950492/13029007
    #     """

    #     value = super().__getattribute__(name)

    #     if isinstance(value, cls):
    #         value = value.value

    #     return value

    # ------------------------------------------------------------

    def to_dict(cls) -> dict[str, typing.Any]:
        """Return the values available on the Enum"""

        return {
            item.name : item.value
            for item in cls
        }

    # ------------------------------------------------------------

    @property
    def __values__(cls) -> list[typing.Any]:
        """Return the values available on the Enum"""

        return [
            item.value
            for item in cls
        ]

    # ------------------------------------------------------------

    @property
    def __names__(cls) -> list[typing.Any]:
        """Return the name available on the Enum"""

        return [
            item.name
            for item in cls
        ]

    # ------------------------------------------------------------

    # TODO check this later, entering recursive call
    # def __repr__(self):
    #     """Representation String"""

    #     return f"{self.__class__.__name__}.{self.name}"