from dataclasses import dataclass
from enum import Enum
from typing import Optional


class SlackButtonStyle(str, Enum):

    primary = "primary"
    danger = "danger"


@dataclass
class SlackButton:

    text: str
    link: Optional[str] = None
    style: Optional[SlackButtonStyle] = None
