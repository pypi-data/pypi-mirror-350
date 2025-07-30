import copy
from typing import Dict, List

from .utils import box_util


class TableBlockV1_0:
    def __init__(self, detect_method, blocks: List[Dict] = [], config: Dict = {}):
        if detect_method not in {"ocr", "elec"}:
            raise ValueError("detect_method should be one of {'ocr', 'elec'}")
        self.detect_method = detect_method
        self.blocks = copy.deepcopy(blocks)
        self.__config = copy.deepcopy(config)

    @staticmethod
    def from_dict(dict_, config={}):
        assert str(dict_["header"]["version"]).startswith("1.0")
        return __class__(
            detect_method=dict_["header"]["detect_method"],
            blocks=dict_.get("tables", []),
            config=config,
        )

    def to_dict(self):
        for block, box in zip(self.blocks, self.tables):
            block["box"] = box
        dict_ = {"header": self.header, "tables": self.blocks}
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
    def cells(self):
        return [cell for block in self.blocks for cell in block["cells"]]

    @property
    def tables(self):
        return [box_util.bounding_box(block["cells"]) for block in self.blocks]
