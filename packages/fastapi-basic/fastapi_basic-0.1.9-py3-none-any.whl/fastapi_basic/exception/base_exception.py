from fastapi import HTTPException
from fastapi import status


class InternalBaseException(HTTPException):
    def __init__(self, status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR, code: str = "internal_server_error",
                 message: str = "Internal server error", **kwargs):
        detail = {
            "code": code,
            "message": message,
            "data": kwargs,
        }
        super().__init__(status_code=status_code, detail=detail)

class LineBotException(HTTPException):
    def __init__(self, status_code: int = status.HTTP_502_BAD_GATEWAY, code: str = "line_bot_error",
                 message: str = "Line bot error", **kwargs):
        detail = {
            "code": code,
            "message": message,
            "data": kwargs,
        }
        super().__init__(status_code=status_code, detail=detail)
