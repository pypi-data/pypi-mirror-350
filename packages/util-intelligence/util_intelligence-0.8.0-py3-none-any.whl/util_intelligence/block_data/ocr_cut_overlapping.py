from typing import Literal

import numpy as np


def ocr_cut_overlapping(text_block, target_key: Literal['texts', 'chars'] = 'chars'):
    boxes = np.array(list(map(lambda char_item: char_item['box'], text_block[target_key])))

    if len(boxes) == 0:
        return text_block

    boxes_0_squeezed = np.expand_dims(boxes, axis=0)
    boxes_1_squeezed = np.expand_dims(boxes, axis=1)
    intersection_w = (
        np.minimum(boxes_0_squeezed[..., 2], boxes_1_squeezed[..., 2])
        - np.maximum(boxes_0_squeezed[..., 0], boxes_1_squeezed[..., 0])
    ).clip(min=0)
    intersection_h = (
        np.minimum(boxes_0_squeezed[..., 3], boxes_1_squeezed[..., 3])
        - np.maximum(boxes_0_squeezed[..., 1], boxes_1_squeezed[..., 1])
    ).clip(min=0)
    intersection = intersection_w * intersection_h
    intersection = np.triu(intersection)
    intersection[np.eye(len(boxes), dtype=bool)] = 0

    boxes_cut = boxes.copy()

    for i, j in zip(*np.where(intersection != 0)):
        box_i, box_j = boxes[i], boxes[j]
        if (min(box_i[3], box_j[3]) - max(box_i[1], box_j[1])) / (
            max(box_i[3], box_j[3]) - min(box_i[1], box_j[1])
        ) > 0.25:
            box_width_i = box_i[2] - box_i[0]
            box_width_j = box_j[2] - box_j[0]
            if (box_i[0] + box_i[2]) > (box_j[0] + box_j[2]):
                (i, box_i), (j, box_j) = (j, box_j), (i, box_i)
            # left: i, right: j
            cut_pos = (box_i[2] * box_width_j + box_j[0] * box_width_i) / (
                box_width_i + box_width_j
            )
            boxes_cut[i][2] = min(boxes_cut[i][2], cut_pos)
            boxes_cut[j][0] = max(boxes_cut[j][0], cut_pos)
        else:
            box_height_i = box_i[3] - box_i[1]
            box_height_j = box_j[3] - box_j[1]
            if (box_i[1] + box_i[3]) > (box_j[1] + box_j[3]):
                (i, box_i), (j, box_j) = (j, box_j), (i, box_i)
            # up: i, down: j
            cut_pos = (box_i[3] * box_height_j + box_j[1] * box_height_i) / (
                box_height_i + box_height_j
            )
            boxes_cut[i][3] = min(boxes_cut[i][3], cut_pos)
            boxes_cut[j][1] = max(boxes_cut[j][1], cut_pos)

    for char_item, box_cut in zip(text_block[target_key], boxes_cut.tolist()):
        char_item['box'] = box_cut

    return text_block
