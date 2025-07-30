import random
from enum import IntEnum
from pathlib import Path
from typing import Callable, List, Optional, Tuple

import cv2
import numpy as np
from PIL.Image import Image

from .color import ColorBGR


class ColorMode(IntEnum):
    UNCHANGED = cv2.IMREAD_UNCHANGED
    GRAY = cv2.IMREAD_GRAYSCALE
    COLOR = cv2.IMREAD_COLOR


def transparent2white(img):
    img = cv2.imdecode(np.frombuffer(img, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
    if img.shape[2] == 4:
        img[np.where(img[:, :, 3] == 0)] = (255, 255, 255, 255)
        img = img[:, :, :3]
    _, img = cv2.imencode('.png', img)
    return img.tobytes()


def imdecode(
    image: str | Path | bytes | np.ndarray | Image,
    mode: ColorMode | int = ColorMode.UNCHANGED,
) -> np.ndarray:
    """
    read image to ndarray for cv2 processing.
    """
    if isinstance(image, np.ndarray):
        if mode == ColorMode.UNCHANGED:
            return image
        return cv2.imdecode(image.astype(np.uint8), mode)

    if isinstance(image, bytes):
        return cv2.imdecode(np.frombuffer(image, dtype=np.uint8), mode)

    elif isinstance(image, str):
        if Path(image).exists():
            return cv2.imread(image, flags=mode)
        else:
            raise FileNotFoundError()

    elif isinstance(image, Path):
        if image.exists():
            return cv2.imread(str(image), flags=mode)
        else:
            raise FileNotFoundError()

    if isinstance(image, Image):
        raise NotImplementedError()
    else:
        raise NotImplementedError()


def imencode(image: np.ndarray, format="png"):
    _, data = cv2.imencode(f".{format}", image)
    return data.tobytes()


def color2gray(image: np.ndarray, retain_dim: bool = False):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    if retain_dim:
        return cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    else:
        return image


def imshow(image: np.ndarray, winname="temp") -> None:
    cv2.imshow(winname, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def imwrite(
    image: np.ndarray | bytes | Image | str | Path,
    save_to: str | Path = "temp.jpg",
) -> None:
    """
    save image to path
    """
    cv2.imwrite(str(save_to), imdecode(image).astype(np.uint8))


def rotate_image(
    image: np.ndarray,
    angle: float = 0,
    center: Optional[Tuple[float, float]] = None,
    resize: float = 1.0,
    borderValue: Tuple = ColorBGR.LIGHTGRAY,
    borderMode: int = cv2.BORDER_CONSTANT,
    clockwise: bool = False,  # 默认是逆时针转的
) -> Tuple[np.ndarray, np.ndarray]:
    """以 center 为中心，顺时针或逆时针旋转 angle 度"""
    if clockwise is True:
        angle = -angle
    h, w = image.shape[:2]
    cX, cY = (w // 2, h // 2) if center is None else center
    M = cv2.getRotationMatrix2D((cX, cY), angle, resize)
    cos, sin = np.abs(M[0, 0]), np.abs(M[0, 1])
    nW, nH = int((h * sin) + (w * cos)), int((h * cos) + (w * sin))
    M[0, 2] += (nW / 2) - cX
    M[1, 2] += (nH / 2) - cY
    image = cv2.warpAffine(
        image,
        M,
        (nW, nH),
        borderValue=borderValue,
        borderMode=borderMode,
    )
    return image, M


def crop_image(image: np.ndarray, box: List[float]):
    h, w = image.shape[:2]
    l, t, r, b = box
    l, t, r, b = [max(0, int(l)), max(0, int(t)), min(int(r), w), min(int(h), b)]
    return image[t:b, l:r]


def resize_image(
    image: np.ndarray,
    max_size: int,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    缩放至最大边长等于 max_size, 返回缩放后的图片和缩放比例
    """
    height, width, *_ = image.shape
    if height > width:
        h, w = max_size, round(width * max_size / height)
    else:
        w, h = max_size, round(height * max_size / width)
    scale = np.array([w / width, h / height])
    return cv2.resize(image, (w, h), interpolation=cv2.INTER_LINEAR), scale


def scale_image(
    image_array: np.ndarray,
    scale_ratio: float,
) -> np.ndarray:
    """
    按比例缩放
    """
    width = int(round(image_array.shape[1] * scale_ratio))
    height = int(round(image_array.shape[0] * scale_ratio))
    return cv2.resize(image_array, (width, height), interpolation=cv2.INTER_LINEAR)


def pad_image_to_square(
    image: np.ndarray,
    max_size,
    border: int = cv2.BORDER_CONSTANT,
    border_value: Tuple = ColorBGR.LIGHTGRAY,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    h, w, *_ = image.shape
    l, t = round((max_size - w) / 2), round((max_size - h) / 2)
    r, b = l + w, t + h
    offset = np.array([l, t])
    return (
        cv2.resize(
            cv2.copyMakeBorder(image, t, t, l, l, border, value=border_value),
            (max_size, max_size),
        ),
        np.array([l, t, r, b]),
        offset,
    )


def shear_image(
    image: np.ndarray,
    src_points,
    dst_points,
) -> Tuple[np.ndarray, np.ndarray]:
    # NOT TESTED
    pts0 = np.float32(src_points).reshape(-1, 2)
    pts1 = np.float32(dst_points).reshape(-1, 2)
    M = cv2.getPerspectiveTransform(pts0, pts1)
    return cv2.warpPerspective(image, M, image.shape[:2]), M


def choose_random_border() -> int:
    return random.choice(
        [
            cv2.BORDER_CONSTANT,
            cv2.BORDER_DEFAULT,
            cv2.BORDER_REFLECT,
            cv2.BORDER_WRAP,
        ]
    )


def get_binary_mask(
    image: np.ndarray,
    threshold: float = 1.0,
) -> np.ndarray:
    gray = imdecode(image, mode=ColorMode.GRAY)
    retval, _ = cv2.threshold(
        255 - gray,
        0,
        255,
        cv2.THRESH_OTSU,  # automatically calculates the optimal threshold
    )
    filter_condition = int(retval * threshold) if retval < 20 else retval
    if filter_condition == 0:
        return np.zeros_like(gray)
    _, mask_img = cv2.threshold(
        255 - gray,
        filter_condition,
        255,
        cv2.THRESH_BINARY,
    )
    return mask_img


def normalize_grayscale(gray: np.ndarray) -> np.ndarray:
    min_val, max_val = gray.min(), gray.max()
    gray_norm = np.zeros_like(gray)
    if min_val != max_val:
        gray_norm = (gray - min_val) * (255 / (max_val - min_val))
    return gray_norm.astype(np.uint8)


def get_projection(image: np.ndarray, axis=0) -> np.ndarray:
    """axis=0 是垂直方向的投影"""
    _, binary = cv2.threshold(image, 0, 1, cv2.THRESH_BINARY)
    projection = binary.sum(axis=axis)
    return projection


def get_projection_target_scopes(
    projection, thresh_fn: Callable, gap_thresh=4, **kwargs
) -> List[Tuple[int, int]]:
    gap_indices = np.where(thresh_fn(projection, **kwargs))[0]
    gap_ends = np.append(
        np.where(np.diff(gap_indices) > 1)[0],
        len(gap_indices) - 1,
    )
    gap_starts = np.insert(gap_ends + 1, 0, 0)[:-1]
    mask = gap_ends - gap_starts >= gap_thresh
    p0s, p1s = gap_indices[gap_starts[mask]], gap_indices[gap_ends[mask]]
    target_scopes = []
    for i, (start, end) in enumerate(zip(p0s, p1s)):
        target_scopes.append((start, end))
    return target_scopes


def get_projection_cret_box(
    binary_image: np.ndarray,
    compare_fn: Callable,
    axis=0,
    gap_thresh=4,
    coefficient=0,
):
    size = binary_image.shape[axis]
    proj = binary_image.sum(axis=axis)
    gap_indices = np.where(compare_fn(proj, coefficient))[0]
    gap_ends = np.append(
        np.where(np.diff(gap_indices) > 1)[0],
        len(gap_indices) - 1,
    )
    gap_starts = np.insert(gap_ends + 1, 0, 0)[:-1]
    mask = gap_ends - gap_starts > gap_thresh
    p0s, p1s = gap_indices[gap_starts[mask]], gap_indices[gap_ends[mask]]
    cret_boxes = []
    if axis == 0:
        for i, (start, end) in enumerate(zip(p0s, p1s)):
            cret_boxes.append([start, 0, end, size])
    else:
        for i, (start, end) in enumerate(zip(p0s, p1s)):
            cret_boxes.append([0, start, size, end])
    return cret_boxes, proj


def pad_image(image, ref_size: int | tuple, value=255, mode=None):
    mode = mode or 'top,left'
    if not isinstance(ref_size, tuple):
        ref_size = ref_size, ref_size
    if image.shape[:2] == ref_size:
        return image
    result = np.full(shape=(*ref_size, *image.shape[2:]), fill_value=value, dtype=image.dtype)
    aligny, alignx = mode.split(',')
    if aligny == 'top':
        y = 0
    elif aligny == 'center':
        y = (result.shape[0] - image.shape[0]) // 2
    elif aligny == 'bottom':
        y = result.shape[0] - image.shape[0]
    if alignx == 'left':
        x = 0
    elif alignx == 'center':
        x = (result.shape[1] - image.shape[1]) // 2
    elif alignx == 'right':
        x = result.shape[1] - image.shape[1]
    result[y : y + image.shape[0], x : x + image.shape[1]] = image
    return result


def ensure_image_size(image, ref_size, value=255, mode=None):
    if not isinstance(ref_size, tuple):
        ref_size = ref_size, ref_size
    if image.shape[0] < ref_size[0] or image.shape[1] < ref_size[1]:
        image = pad_image(
            image,
            tuple(max(x, y) for x, y in zip(image.shape[:2], ref_size)),
            value,
            mode,
        )
    return image


def cut_image(image, box):

    def slice2d(value, box, fill_value):
        if 0 <= box[0] <= box[2] <= value.shape[1] and 0 <= box[1] <= box[3] <= value.shape[0]:
            return value[box[1] : box[3], box[0] : box[2]]
        else:
            result = np.full(
                (box[3] - box[1], box[2] - box[0], *value.shape[2:]),
                fill_value,
                value.dtype,
            )
            x0, y0 = max(box[0], 0), max(box[1], 0)
            x1, y1 = min(box[2], value.shape[1]), min(box[3], value.shape[0])
            ox, oy = x0 - box[0], y0 - box[1]
            w, h = x1 - x0, y1 - y0
            if w < 0 or h < 0:
                return result
            else:
                result[oy : oy + h, ox : ox + w] = value[y0:y1, x0:x1]
            return result

    x0, y0, x1, y1 = box
    x0, y0 = max(int(x0), 0), max(int(y0), 0)
    x1, y1 = int(round(x1)), int(round(y1))
    x1 = max(x1, x0 + 4)
    y1 = max(y1, y0 + 4)
    return slice2d(image, (x0, y0, x1, y1), 255)


def cut_image_with_extent(image, box):
    x0, y0, x1, y1 = box['box']
    width, height = x1 - x0, y1 - y0
    margin_x = max(2, width // 8)
    margin_top = height // 8
    margin_bottom = max(height // 8, 3)
    cbox = [x0 - margin_x, y0 - margin_top, x1 + margin_x, y1 + margin_bottom]
    part_image = cut_image(image, cbox)
    if part_image.size > 0:
        return part_image, cbox
    else:
        raise ValueError('part_image is empty')


def paste_image(background, foreground, offset, method='overwrite'):
    if offset[0] < 0 or offset[1] < 0:
        foreground = foreground[max(-offset[1], 0) :, max(-offset[0], 0) :]
        offset = np.maximum(offset, 0)
    height = min(background.shape[0] - offset[1], foreground.shape[0])
    width = min(background.shape[1] - offset[0], foreground.shape[1])
    if len(offset) == 4:
        width = min(width, offset[2] - offset[0])
        height = min(height, offset[3] - offset[1])
    if width <= 0 or height <= 0:
        return False
    background = background[offset[1] : offset[1] + height, offset[0] : offset[0] + width]
    foreground = foreground[:height, :width]
    if method == 'overwrite':
        background[...] = foreground
    elif method == 'max':
        np.maximum(background, foreground, out=background)
    elif method == 'min':
        np.minimum(background, foreground, out=background)
    else:
        raise NotImplementedError(f'{method} is not implemented.')
    return True


def blend_image(background, foreground, opacity, offset):
    if offset[0] < 0 or offset[1] < 0:
        foreground = foreground[max(-offset[1], 0) :, max(-offset[0], 0) :]
        opacity = opacity[max(-offset[1], 0) :, max(-offset[0], 0) :]
        offset = np.maximum(offset, 0)
    height = min(background.shape[0] - offset[1], foreground.shape[0])
    width = min(background.shape[1] - offset[0], foreground.shape[1])
    if len(offset) == 4:
        width = min(width, offset[2] - offset[0])
        height = min(height, offset[3] - offset[1])
    if width <= 0 or height <= 0:
        return False
    background = background[offset[1] : offset[1] + height, offset[0] : offset[0] + width]
    foreground, opacity = foreground[:height, :width], opacity[:height, :width, None].astype(
        np.int32
    )
    background[...] = (background * (255 - opacity) + foreground * opacity) // 255
    return True


def align_image(image: np.ndarray, blocksize: tuple | int, padding=255):
    def align(value, size):

        mod = value % size
        return value + (size - mod) % size

    shape = image.shape
    if isinstance(blocksize, tuple):
        blockheight, blockwidth = blocksize
    else:
        blockwidth = blockheight = blocksize
    aligned_height = align(shape[0], blockheight)
    aligned_width = align(shape[1], blockwidth)
    result = np.full(
        shape=(aligned_height, aligned_width, *image.shape[2:]),
        fill_value=padding,
        dtype=image.dtype,
    )
    result[: image.shape[0], : image.shape[1], ...] = image
    return result


def apply_brightness_contrast(image, brightness=255, contrast=127):
    # recommend settings: brightness ~[-130~130], contrast~[-70~10]
    if brightness != 0:
        if brightness > 0:
            shadow = brightness
            highlight = 255
        else:
            shadow = 0
            highlight = 255 + brightness
        alpha_b = (highlight - shadow) / 255
        gamma_b = shadow

        buf = cv2.addWeighted(image, alpha_b, image, 0, gamma_b)
    else:
        buf = image.copy()

    if contrast != 0:
        f = float(131 * (contrast + 127)) / (127 * (131 - contrast))
        alpha_c = f
        gamma_c = 127 * (1 - f)
        buf = cv2.addWeighted(buf, alpha_c, buf, 0, gamma_c)
    return buf
