from typing import Optional


class CodeMessageException(Exception):
    """
    내부 모듈에 사용
    """

    default_message = "모듈 에러가 발생했습니다"
    default_code = "_error"

    def __init__(
        self, code=None, msg: Optional[str] = None, context: Optional[dict] = None
    ):
        self.code = code or self.default_code
        self.msg: Optional[str] = msg or self.default_message
        self.context: Optional[dict] = context or {}
        message = f"code {code}.{msg}"
        super().__init__(message)

    def __str__(self):
        return "<{class_name} code: {code} message: {message}>".format(
            class_name=self.__class__.__name__,
            code=self.code,
            message=self.msg,
        )


class LoginException(CodeMessageException):
    default_message = "로그인 실패"
    default_code = "_login"


class NoAttrException(CodeMessageException):
    default_message = "필수 속성이 없습니다"
    default_code = "_noattr"


class NotOkException(CodeMessageException):
    default_message = "요청에 대한 응답이 올바르지 않습니다"
    default_code = "_request"
