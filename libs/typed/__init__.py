import typing


class ResultDict(typing.TypedDict):
    status: int
    msg: str
    data: list
