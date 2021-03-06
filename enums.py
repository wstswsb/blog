from enum import IntEnum


class TokenType(IntEnum):
    ACCESS = 1
    REFRESH = 2


class TimeConstants(IntEnum):
    SECOND = 1
    MINUTE = 60
    QUARTER_OF_AN_HOUR = 900
    HOUR = 3600
    DAY = 86400
    MOUNTH = 2592000  # 30 days


class ActionType(IntEnum):
    GET_POST_PAGE = 1
    GET_POST_BY_ID = 2
    DELETE_POST_BY_ID = 3
    CREATE_POST = 4
    UPDATE_POST = 5
