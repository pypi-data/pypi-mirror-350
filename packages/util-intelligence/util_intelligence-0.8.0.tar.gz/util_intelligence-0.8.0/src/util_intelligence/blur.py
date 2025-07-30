import copy
import random
from typing import Callable, List, Tuple

import cv2
import numpy as np

from .image_util import ColorMode, imdecode


def __norm_range(range_: Tuple[int, int]):
    a, b = min(range_), max(range_)
    if b < 0:
        return (0, 1)
    if a < 0:
        return __norm_range((0, b))
    if a == b:
        return (a, a + 1)
    return (a, b)


def apply_gauss_blur(img: np.ndarray, kernel_range: Tuple[int, int] = (3, 6)):
    ksize = random.choice(range(*__norm_range(kernel_range)))
    sigma = random.choice(range(3)) if ksize <= 3 else 0
    img = cv2.GaussianBlur(img, (ksize, ksize), sigma)
    return img


def apply_norm_blur(img: np.ndarray, kernel_range: Tuple[int, int] = (2, 4)):
    ksize = random.choice(range(*__norm_range(kernel_range)))
    img = cv2.blur(img, (ksize, ksize))
    return img


def apply_compression_blur(image: np.ndarray, quality_range: Tuple[int, int] = (40, 90)):
    _, _data = cv2.imencode(
        ".jpg",
        image,
        [
            cv2.IMWRITE_JPEG_QUALITY,
            random.choice(range(*__norm_range(quality_range))),
        ],
    )
    image = imdecode(_data.tobytes(), ColorMode.COLOR if image.ndim >= 3 else ColorMode.GRAY)
    return image


def apply_blur(
    img: np.ndarray,
    funcs_with_weights: List[Tuple[Callable, int]] = [
        (lambda x: x, 1),
        (apply_gauss_blur, 2),
        (apply_norm_blur, 2),
        (apply_compression_blur, 2),
    ],
    choices_range: Tuple[int, int] = (1, 2),
):
    _img = copy.deepcopy(img)
    funcs, weights = list(zip(*funcs_with_weights))
    funcs = random.choices(
        funcs,
        weights=weights,
        k=random.choice(range(*__norm_range(choices_range))),
    )
    for func in funcs:
        _img = np.clip(func(_img), 0, 255).astype(np.uint8)
    return _img
