from typing import List, Literal, Optional, TypedDict

_Box = List[int | float]
_DetectMethod = Literal["elec", "ocr"]


class HeaderDict(TypedDict):
    version: str
    detect_method: _DetectMethod


class BoxDict(TypedDict):
    box: _Box


class TextBoxDict(TypedDict):
    text: str
    box: _Box


class TableBoxDict(TypedDict):
    cells: List[_Box]
    box: _Box


class ImageBoxDict(TypedDict):
    image: bytes
    box: _Box


class CharBlockDict(TypedDict):
    header: HeaderDict
    width: Optional[float]
    height: Optional[float]
    chars: List[TextBoxDict]


class TextBlockDict(TypedDict):
    header: HeaderDict
    width: Optional[float]
    height: Optional[float]
    texts: List[TextBoxDict]


class LineBlockDict(TypedDict):
    header: HeaderDict
    width: Optional[float]
    height: Optional[float]
    lines: List[BoxDict]


class TableBlockDict(TypedDict):
    header: HeaderDict
    width: Optional[float]
    height: Optional[float]
    tables: List[TableBoxDict]


class ImageBlockDict(TypedDict):
    header: HeaderDict
    width: Optional[float]
    height: Optional[float]
    images: List[ImageBoxDict]


class MaskingBlock(TypedDict):
    width: float
    height: float
    maskings: List[BoxDict]
