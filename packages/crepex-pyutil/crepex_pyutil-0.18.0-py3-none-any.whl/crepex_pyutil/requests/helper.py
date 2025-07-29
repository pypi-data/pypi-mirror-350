import os
import pickle
from json.decoder import JSONDecodeError
from typing import Any
from typing import Callable
from typing import Optional

from requests import Response
from requests import Session
from requests.adapters import HTTPAdapter
from requests.utils import cookiejar_from_dict
from requests.utils import dict_from_cookiejar
from urllib3.util.retry import Retry

from ..exceptions import NotOkException


class AbstractRequestHelper:
    logger: Optional[Callable[[str, Any], Any]] = None

    def __init__(self):
        self._init_session()

    def _init_session(self):
        self.session = Session()
        self.session.mount(
            "https://",
            HTTPAdapter(
                max_retries=Retry(
                    total=3,
                    backoff_factor=0.1,
                    status_forcelist=[500, 502, 503, 504],
                )
            ),
        )

    def set_logger(self, logger: Optional[Callable[[str, Any], Any]]):
        self.logger = logger

    @property
    def use_saved_session(self):
        return True

    @property
    def session_file_name(self):
        return os.path.join(
            os.path.split(__file__)[0],
            f"_session_{self.__class__.__name__}",
        )

    def _save_session_to_file(self):
        with open(self.session_file_name, "wb") as file:
            pickle.dump(dict_from_cookiejar(self.session.cookies), file)

    def _load_session_from_file(self):
        with open(self.session_file_name, "rb") as file:
            self.session.cookies = cookiejar_from_dict(pickle.load(file))

    def logging_response_error(self, msg: str, data=None):
        if self.logger:
            self.logger(msg, data)

    def get_response(self, res: Response, code=400, extra_ok=False):
        if not res.ok and not extra_ok:
            self.logging_response_error(msg=f"{code}")
            raise NotOkException(code=code)
        return res

    def get_response_json(
        self, res: Response, extra_ok=False, error_msg="응답이 올바르지 않습니다"
    ):
        try:
            data = res.json()
            ctx = {
                "status_code": res.status_code,
                "message": data.get("message", ""),
            }
            if isinstance(data, dict):
                ctx.update(data)
            else:
                ctx["data"] = data
            if not res.ok and not extra_ok:
                self.logging_response_error(msg=error_msg, data=ctx)
                raise NotOkException(msg=error_msg, context=ctx)
            return data
        except JSONDecodeError:
            self.logging_response_error(
                msg="JSON Parse error", data={"status": res.status_code}
            )
            raise NotOkException(msg="데이터파싱에 실패했습니다")
