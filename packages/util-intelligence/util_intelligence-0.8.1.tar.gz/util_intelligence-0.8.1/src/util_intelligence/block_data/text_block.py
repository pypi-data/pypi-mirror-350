import copy
import warnings
from functools import lru_cache
from typing import Any, Dict, List, Literal, Optional

import numpy as np
from PIL import ImageFont

from .constants import SIMSUN_FONT_FILE_PATH
from .utils import algorithm, box_util

SortKey = Literal["x0", "y0", "cell", "line"]


class TextBlockV1_0:
    def __init__(
        self,
        detect_method: str,
        chars: Optional[List[Dict]] = None,
        texts: Optional[List[Dict]] = None,
        config: dict = {},
    ):
        assert chars is not None or texts is not None, "chars and texts must not be both None"
        assert detect_method in [
            "ocr",
            "elec",
            "human",
        ], "detect_method must be one of {'ocr', 'elec', 'human'}"
        self.detect_method = detect_method
        self.__chars = copy.deepcopy(chars)
        self.__texts = copy.deepcopy(texts)
        self.__config = copy.deepcopy(config)

    @staticmethod
    def from_dict(dict_, config={}):
        assert dict_["header"]["version"] == "1.0"
        return __class__(
            detect_method=dict_["header"]["detect_method"],
            chars=dict_.get("chars"),
            texts=dict_.get("texts"),
            config=config,
        )

    def to_dict(self) -> Dict[str, Any]:
        dict_ = {"header": self.header}
        if self.__chars is not None:
            dict_["chars"] = self.__chars  # type: ignore
        if self.__texts is not None:
            dict_["texts"] = self.__texts  # type: ignore
        return dict_

    @property
    def header(self):
        return {
            "version": "1.0",
            "detect_method": self.detect_method,
        }

    @property
    def config(self):
        return self.__config

    @property
    def chars(self):
        if self.__chars is not None:
            return self.__chars
        else:
            assert self.__texts is not None
            chars = []
            for text in self.__texts:
                chars += __class__.approxymate_chars_from_text(text, self._load_simsun_font())
            for char in chars:
                char.update({"conf": 1.0, "prob": [1.0]})
            return chars

    @chars.setter
    def chars(self, chars):
        self.__chars = chars

    @staticmethod
    def approxymate_chars_from_text(text, font):
        if len(text["text"]) == 0:
            warnings.warn(f"text item with empty text string, box={text['box']}")
            return []

        text_x0, text_y0, text_x1, text_y1 = text["box"]
        char_width_weights = np.array([font.getsize(c)[0] for c in text["text"]])
        if not (char_width_weights == 0).all():
            char_widths = char_width_weights / char_width_weights.sum() * (text_x1 - text_x0)
        else:
            char_widths = np.full_like(
                char_width_weights,
                fill_value=(text_x1 - text_x0) / len(char_width_weights),
            )
        char_xs = (np.insert(np.cumsum(char_widths), 0, 0) + text_x0).tolist()
        chars = [
            {"text": c, "box": [char_xs[i], text_y0, char_xs[i + 1], text_y1]}
            for i, c in enumerate(text["text"])
        ]
        return chars

    @lru_cache
    def _load_simsun_font(self):
        return ImageFont.truetype(SIMSUN_FONT_FILE_PATH, 32)

    @property
    def texts(self):
        if self.__texts is not None:
            return self.__texts
        else:
            assert self.__chars is not None
            return [
                __class__.merge_items(char_group, sort_key="line")
                for char_group in self.group_items_with_position(
                    self.__chars,
                    self.__config.get("text_merge_distance", 0.25),
                    self.__config.get("text_merge_variance", 0.25),
                )
            ]

    @property
    def texts_with_ordered_chars(self):
        assert self.__chars is not None
        grouped_ordered_chars = [
            __class__.sorted_items(char_group, key="line")
            for char_group in self.group_items_with_position(
                self.__chars,
                self.__config.get("text_merge_distance", 0.25),
                self.__config.get("text_merge_variance", 0.25),
            )
        ]
        texts = [
            {
                "text": "".join([item["text"] for item in char_group]),
                "box": __class__.merge_boxes([item["box"] for item in char_group]),
                "chars": char_group,
            }
            for char_group in grouped_ordered_chars
        ]
        return texts

    @texts.setter
    def texts(self, texts):
        self.__texts = texts

    @property
    def lines(self):
        return [
            __class__.merge_items(text_group, sort_key="x0", seperator=" ")
            for text_group in self.group_items_with_position(
                self.texts,
                self.__config.get("paragraph_merge_distance", 4),
                self.__config.get("paragraph_merge_variance", 0.25),
            )
        ]

    @staticmethod
    def group_items_with_position(
        items, x_gap_threshold=2, y_gap_threshold=0.25, y_iou_threshold=2 / 3
    ):
        def __compute_relation(box0, box1):
            if not __class__._in_sameline(box0, box1, y_gap_threshold=y_gap_threshold):
                return 2
            if __class__._is_adjacent(box0, box1, x_gap_threshold, y_iou_threshold=y_iou_threshold):
                return 0
            else:
                return 1  # possible subscript characters

        if len(items) == 0:
            return []
        argsort_y = np.argsort([(x["box"][1] + x["box"][3]) / 2 for x in items])
        relation = algorithm.DisjointSet()
        for index_i, i in enumerate(argsort_y):
            box0 = items[i]
            for index_j, j in enumerate(argsort_y[index_i + 1 :]):
                box1 = items[j]
                r = __compute_relation(box0["box"], box1["box"])
                if r == 0:
                    relation.union([i, j])
                elif r == 2:
                    break
        groups = list(relation.groups(len(items)).values())
        item_groups = [[items[x] for x in g] for g in groups]
        return item_groups

    @staticmethod
    def _in_sameline(box0, box1, y_gap_threshold=0.25):
        cy0 = (box0[1] + box0[3]) / 2
        cy1 = (box1[1] + box1[3]) / 2
        reference = box0[3] - box0[1]
        return reference > 0 and abs(cy0 - cy1) / reference <= y_gap_threshold

    @staticmethod
    def _is_adjacent(box0, box1, x_gap_threshold=1, y_iou_threshold=2 / 3):
        o, _, _, m = box_util.overlap(box0[1], box0[3], box1[1], box1[3])
        if m > 0 and o / m >= y_iou_threshold:
            o1, *_ = box_util.overlap(box0[0], box0[2], box1[0], box1[2])
            return o1 / m >= -x_gap_threshold
        else:
            return False

    @staticmethod
    def merge_items(items, sort_key: SortKey = "x0", seperator=""):
        __class__.sort_items(items, key=sort_key)
        texts, boxes = zip(*[(item["text"], item["box"]) for item in items])
        return {
            "text": seperator.join(texts),
            "box": __class__.merge_boxes(boxes),
        }

    @staticmethod
    def merge_boxes(boxes):
        x0s, y0s, x1s, y1s = zip(*boxes)
        return [min(x0s), np.mean(y0s).item(), max(x1s), np.mean(y1s).item()]

    @staticmethod
    def sort_items(items, key: SortKey = "x0"):
        if key == "x0":
            items.sort(key=lambda item: item["box"][0])
        elif key == "y0":
            items.sort(key=lambda item: item["box"][1])
        elif key == "cell":
            algorithm.bubble_sort(items, cmp=box_util.cell_cmp, key=lambda item: item["box"])
        elif key == "line":
            algorithm.bubble_sort(items, cmp=box_util.line_cmp, key=lambda item: item["box"])
        else:
            raise ValueError('key must be one of {"x0", "y0", "cell", "line"}')

    @staticmethod
    def sorted_items(items, key: SortKey = "x0"):
        items = copy.deepcopy(items)
        __class__.sort_items(items, key=key)
        return items

    @staticmethod
    def group_items_with_regions(items, regions):
        region_item_groups = []
        free_status_list = [True for _ in items]
        for region in regions:
            region_item_group = []
            for i, item in enumerate(items):
                if free_status_list[i] and __class__._is_inside(item["box"], region):
                    region_item_group.append(item)
                    free_status_list[i] = False
            region_item_groups.append(region_item_group)
        free_items = [item for i, item in enumerate(items) if free_status_list[i]]
        return region_item_groups, free_items

    @staticmethod
    def _is_inside(box, region):
        if not isinstance(box, np.ndarray):
            box = np.array(box)
        x0, y0, x1, y1 = region
        if box.ndim == 1:
            cx = (box[0] + box[2]) / 2
            cy = (box[1] + box[3]) / 2
        else:
            cx, cy = box.mean(0)
        return x0 <= cx < x1 and y0 <= cy < y1
