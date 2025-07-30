from dataclasses import dataclass
from dataclasses import field
from enum import Enum

__all__ = [
    'ClcNote',
]


class MarkupLang(Enum):
    CLEANCOPY = 'cleancopy'
    MARKDOWN = 'markdown'
    RST = 'rst'


@dataclass(frozen=True, slots=True)
class DocNote:
    value: str
    lang: MarkupLang | None = field(kw_only=True)


@dataclass(frozen=True, slots=True)
class ClcNote:
    value: str
    lang: MarkupLang = MarkupLang.CLEANCOPY
