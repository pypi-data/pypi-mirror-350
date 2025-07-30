import json
from types import NoneType


class Response:
    def __init__(
        self,
        success: bool = True,
        msg: str | NoneType = None,
        data: list = [],
        page: dict | NoneType = None,
    ):
        try:
            assert type(success) == bool, "success is not boolean"
            self.success = success
            assert (
                a := type(msg)
            ) == str or a == NoneType, "msg is not string or None Type"
            self.msg = msg
            assert type(data) == list, "data is not list/array"
            self.data = data
            assert (
                a := type(page)
            ) == dict or a == NoneType, "page is not dict(object)"
            self.page = page

        except Exception as e:
            self.success = False
            self.msg = str(e)
            self.data = []
            self.page = None

    def __str__(self):
        return json.dumps(
            {
                "success": self.success,
                "msg": self.msg,
                "data": self.data,
                "page": self.page,
            }
        )

    @property
    def json(self):
        json = {
            "success": str(self.success).lower(),
            "msg": self.msg,
            "data": self.data,
        }
        if self.page:
            json["page"] = self.page

        return json
