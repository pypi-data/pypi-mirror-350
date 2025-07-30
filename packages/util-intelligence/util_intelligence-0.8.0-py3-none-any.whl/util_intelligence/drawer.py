from itertools import cycle
from typing import List, Optional, Sequence, Tuple, Union

import cv2
import numpy as np

from .color import ColorBGR, scope_color


def create_blank_image(
    shape: Sequence[int],
    color: Optional[Union[int, Sequence[int]]] = None,
) -> np.ndarray:

    def fill_gray(color):
        if color is None:
            color = 255
        elif isinstance(color, Sequence) and len(color) == 1:
            color = color[0]

        if isinstance(color, int):
            blank_image.fill(scope_color(color))
        else:
            raise ValueError("Please check parmeter shape or color!")

    def fill_color(color):
        if color is None:
            color = 255, 255, 255
        elif isinstance(color, Sequence) and len(color) == 1:
            color = color, color, color

        if isinstance(color, Sequence) and len(color) == 3:
            color = [scope_color(x) for x in color]
            blank_image[:, :] = color

    blank_image = np.zeros(shape, dtype=np.uint8)
    if len(shape) == 2:
        fill_gray(color)
    elif len(shape) == 3:
        fill_color(color)
    else:
        raise NotImplementedError()

    return blank_image


def draw_ellipse(
    image: np.ndarray,
    center: Tuple[float, float],
    axes: Tuple[float, float],
    angle: float = 0,
    color: Tuple = ColorBGR.BLACK,
    start_angle: float = 0,
    end_angle: float = 360,
    thickness: int = 1,
):
    """angle: 顺时针偏离"""
    _image = np.copy(image)
    cv2.ellipse(
        _image,
        center=tuple(map(int, center)),
        angle=angle,
        axes=tuple(map(int, axes)),
        color=color,
        startAngle=start_angle,
        endAngle=end_angle,
        thickness=thickness,
    )
    return _image


def draw_point(
    image: np.ndarray,
    point: Tuple[float, float],
    color: Tuple = ColorBGR.BLACK,
    thickness: int = 4,
):
    _image = np.copy(image)
    cv2.circle(
        _image,
        center=tuple(map(int, point)),
        radius=1,
        color=color,
        thickness=thickness,
    )
    return _image


def draw_polygon(image, points, color=ColorBGR.BLACK, closed=True, thickness=1):
    _image = np.copy(image)
    cv2.polylines(
        _image,
        [np.array(points, np.int32)],
        isClosed=closed,
        color=color,
        thickness=thickness,
        lineType=cv2.LINE_AA,
    )
    return _image


def put_ascii_texts(
    image: np.ndarray,
    text_items: Sequence[Tuple[str, List]],
    font_scale: float = 1,
    colors: list = [ColorBGR.BLACK],
    thickness=1,
) -> np.ndarray:
    text_image = np.copy(image)
    color_cycle = cycle(colors)
    for text, (x1, y1, x2, y2) in text_items:
        cv2.putText(
            text_image,
            text,
            org=(int(x1), int(y2)),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=font_scale,
            color=next(color_cycle),
            thickness=thickness,
            lineType=2,
        )
    return text_image


def draw_lines(
    image: np.ndarray,
    lines: Sequence[Sequence[float]],
    colors=[ColorBGR.MAGENTA],
    thickness=1,
    dotted=False,
    gap=5,
) -> np.ndarray:
    def draw_dotted_line(image, pt1, pt2, color, thickness):
        [x1, y1], [x2, y2] = pt1, pt2
        distance = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
        points = []
        for i in np.arange(0, distance, gap):
            r = i / distance
            x = int((x1 * (1 - r) + x2 * r) + 0.5)
            y = int((y1 * (1 - r) + y2 * r) + 0.5)
            points.append([x, y])
        for x, y in points:
            cv2.circle(
                image,
                [x + int(gap / 3), y + int(gap / 3)],
                thickness=thickness,
                color=color,
                radius=1,
            )
        return image

    _image = np.copy(image)
    colors_cycle = cycle(colors)
    for line in np.array(lines, dtype=np.int32):
        x1, y1, x2, y2 = line
        if dotted is True:
            _image = draw_dotted_line(
                _image,
                [x1, y1],
                [x2, y2],
                color=next(colors_cycle),
                thickness=thickness,
            )
        else:
            cv2.line(
                _image,
                [x1, y1],
                [x2, y2],
                color=next(colors_cycle),
                thickness=thickness,
            )
    return _image


def draw_bboxes(
    image: np.ndarray,
    bboxes: Sequence[Sequence[float]],
    colors=[ColorBGR.LIME],
    thickness=1,
):
    _image = np.copy(image)
    colors_cycle = cycle(colors)
    for x1, y1, x2, y2 in np.array(bboxes, dtype=np.int32):
        _image = draw_polygon(
            _image,
            [[x1, y1], [x2, y1], [x2, y2], [x1, y2]],
            color=next(colors_cycle),
            thickness=thickness,
        )
    return _image
