import difflib
import random
from collections import abc, defaultdict
from typing import Iterable, Tuple

import numpy as np


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Line:
    def __init__(self, x0, y0, x1, y1):
        self.k = (y1 - y0) / (x1 - x0)
        self.b = y0 - self.k * x0

    def __call__(self, x):
        return self.k * x + self.b

    def substitude(self, point):
        return point.y - self.__call__(point.x)


class Relation(object):
    def __init__(self):
        self.parents = {}

    def get_parent(self, id):
        if id not in self.parents:
            self.parents[id] = id
        if self.parents[id] != id:
            self.parents[id] = self.get_parent(self.parents[id])
        return self.parents[id]

    def union(self, ids):
        ids = [self.get_parent(id) for id in ids]
        p = min(ids)
        for id in ids:
            self.parents[id] = p

    def groups(self, ids=None):
        if ids is None:
            ids = self.parents.keys()
        elif isinstance(ids, int):
            ids = range(ids)
        result = defaultdict(lambda: [])
        for id in ids:
            result[self.get_parent(id)].append(id)
        return dict(result)


class GraphVertex(object):
    def __init__(self, id, input, cells):
        self.id = id
        self.input = input
        self.states = []
        self.cells = cells


class GraphNode(object):
    def __init__(self, cell: GraphVertex):
        self.parents: Iterable = []
        self.children: Iterable = []
        self.cell = cell


class Graph(object):
    def __init__(self, h, v, cells):
        h = {int(id): cids for id, cids in h.items()}
        v = {int(id): cids for id, cids in v.items()}
        self.ids = list(Graph.collect_ids(h) | Graph.collect_ids(v))
        self.cells = cells
        self.h_children = defaultdict(lambda: [], h)
        self.v_children = defaultdict(lambda: [], v)
        self.h_parents = defaultdict(lambda: [], Graph.inverse_direction(h))
        self.v_parents = defaultdict(lambda: [], Graph.inverse_direction(v))
        self.h_ancestors = self.all_ancestors(self.h_parents)
        self.v_ancestors = self.all_ancestors(self.v_parents)

    def all_ancestors(self, parents):
        r = {}
        for id in self.ids:
            r[id] = Graph.ancestors(parents, id, self.cells)
        return defaultdict(lambda: [], r)

    def relationship(self, pid, id):
        if id in self.h_parents and pid in self.h_parents[id]:
            return 1
        elif id in self.h_ancestors and pid in self.h_ancestors[id]:
            return 2
        elif id in self.v_parents and pid in self.v_parents[id]:
            return 3
        elif id in self.v_ancestors and pid in self.v_ancestors[id]:
            return 4
        else:
            return 0

    def is_vparent(self, pid, id):
        return id in self.v_parents and pid in self.v_parents[id]

    def is_hparent(self, pid, id):
        return id in self.h_parents and pid in self.h_parents[id]

    def flatten_relationship(self):
        for id in self.ids:
            for pid in Graph.ancestors(self.h_ancestors, id, self.cells) | Graph.ancestors(
                self.v_ancestors, id, self.cells
            ):
                yield (pid, id)

    @staticmethod
    def inverse_direction(g):
        imap = {}
        for id, cids in g.items():
            for cid in cids:
                if cid in imap:
                    imap[cid].append(id)
                else:
                    imap[cid] = [id]
        return imap

    @staticmethod
    def collect_ids(g):
        ids = set()
        for id, cids in g.items():
            ids.add(id)
            for cid in cids:
                ids.add(cid)
        return ids

    @staticmethod
    def ancestors(parents, id, cells):
        def _overlap(s0, e0, s1, e1):
            o, t, _, _ = overlap(s0, e0, s1, e1)
            return o / t >= 0.01

        cache = set()
        queue = [id]
        box = cells[id]
        while queue:
            id = queue.pop(0)
            if id in parents:
                for pid in parents[id]:
                    pbox = cells[pid]
                    if _overlap(box[0], box[2], pbox[0], pbox[2]) or _overlap(
                        box[1], box[3], pbox[1], pbox[3]
                    ):
                        if pid not in cache:
                            queue.append(pid)
                            cache.add(pid)
        return cache

    @staticmethod
    def link(vertices, edges, forward):
        graph = {v.id: GraphNode(v) for v in vertices}
        for id, children in edges.items():
            assert isinstance(id, int)
            for cid in children:
                if forward:
                    graph[id].children.append(graph[cid])  # type: ignore
                    graph[cid].parents.append(graph[id])  # type: ignore
                else:
                    graph[id].parents.append(graph[cid])  # type: ignore
                    graph[cid].children.append(graph[id])  # type: ignore
        return graph


def boxes_to_layout(boxes, open_end=True, tolerance=0):
    xpos = []
    ypos = []
    if not open_end:
        boxes = [(box[0], box[1], box[2] + 1, box[3] + 1) for box in boxes]
    for box in boxes:
        xpos += [box[0], box[2]]
        ypos += [box[1], box[3]]
    xpos, ypos = sorted(xpos), sorted(ypos)

    def make_layout(axis):
        last_pos = -tolerance - 1
        index = -1
        mapping = {}
        for pos in axis:
            if pos - last_pos > tolerance:
                index += 1
            mapping[pos] = index
            last_pos = pos
        return mapping

    xmap, ymap = make_layout(xpos), make_layout(ypos)
    result = [(xmap[x0], ymap[y0], xmap[x1], ymap[y1]) for x0, y0, x1, y1 in boxes]
    return result


def diff_large_text(text1: str, text2: str, min_match=5, max_removal=100, window=500):
    offset1, offset2 = 0, 0
    result = []
    while True:
        snip1 = text1[offset1 : offset1 + window]
        snip2 = text2[offset2 : offset2 + window]
        if not snip1 and not snip2:
            break
        blocks, size1, size2 = diff_text(
            snip1, snip2, min_match, max_removal, offset2 + window >= len(text2)
        )
        offset1 += size1
        offset2 += size2
        '''
        if len(blocks) >= 2 and result and result[-1][0] == 'same'\
                and blocks[0][0] == 'remove' and blocks[1][0] == 'add'\
                and blocks[0][1] == blocks[1][1]:
            result[-1][1] += blocks[0][1]
            blocks = blocks[2:]
        '''
        result += blocks
    return result


def diff_text(text1: str, text2: str, min_match, max_removal, last_block) -> Tuple:
    if not text1 and not text2:
        raise ValueError()
    if text1 == text2:
        return [('same', text1)], len(text1), len(text2)
    matcher = difflib.SequenceMatcher(None, text1, text2, False)
    blocks = matcher.get_matching_blocks()
    result = []
    start1, start2 = 0, 0

    def append_block(block, start1, start2, max_size=None):
        max_size = max_size or block.size
        if max_size >= min_match or text1[block.a + max_size : block.a + max_size + 1] in [
            '\n',
            ' ',
        ]:
            if block.a > start1:
                result.append(('remove', text1[start1 : block.a]))
            if block.b > start2:
                result.append(('add', text2[start2 : block.b]))
            result.append(('same', text1[block.a : block.a + max_size]))
            start1 = block.a + max_size
            start2 = block.b + max_size
        return start1, start2

    for block in blocks:
        remain_length = min(len(text1) - block.a - block.size, len(text2) - block.b - block.size)
        if remain_length < max_removal + min_match and not last_block:
            if block.size >= 2 * min_match:
                start1, start2 = append_block(block, start1, start2, block.size - min_match)
            break
        start1, start2 = append_block(block, start1, start2)

    if not result:
        if text1:
            result.append(('remove', text1))
        if text2:
            result.append(('add', text2))
        start1 = len(text1)
        start2 = len(text2)
    return result, start1, start2


def overlap(s0, e0, s1, e1):
    t = (e0 - s0) + (e1 - s1)
    o = min(e0, e1) - max(s0, s1)
    min_length = min(e0 - s0, e1 - s1)
    max_length = max(e0 - s0, e1 - s1)
    return o, t, min_length, max_length


def iou(box0, box1):
    width = min(box0[2], box1[2]) - max(box0[0], box1[0])
    height = min(box0[3], box1[3]) - max(box0[1], box1[1])
    return max(width, 0) * max(height, 0)


def common_box(box0, box1):
    x0 = max(box0[0], box1[0])
    y0 = max(box0[1], box1[1])
    x1 = min(box0[2], box1[2])
    y1 = min(box0[3], box1[3])
    if x0 >= x1 or y0 >= y1:
        return None
    box = (x0, y0, x1, y1)
    if isinstance(box0, np.ndarray) or isinstance(box1, np.ndarray):
        box = np.array(box)
    return box


def area(box):
    if box[0] >= box[2] or box[1] >= box[3]:
        return 0
    return (box[2] - box[0]) * (box[3] - box[1])


def bounding_box(boxes):
    return [
        min(x[0] for x in boxes),
        min(x[1] for x in boxes),
        max(x[2] for x in boxes),
        max(x[3] for x in boxes),
    ]


def containing_box(points):
    if not isinstance(points, np.ndarray):
        points = np.array(points)
    x0, y0 = points.min(0)
    x1, y1 = points.max(0)
    return np.array([x0, y0, x1 + 1, y1 + 1])


def create_dags(cell_text, max_context=10, max_cells=10000):
    dags = []
    context = []
    for type, block, attrib in cell_text:
        if type == 'table':
            if not block:
                continue
            if len(block) >= max_cells:
                print('table cells exceeds max allowed cells.', len(block))
                continue
            dag = create_dag(block)
            dag['context'] = context
            dag['id'] = attrib['id']
            dags.append(dag)
            context = []
        else:
            text = block.strip()
            if text:
                context.append(text)
                if len(context) > max_context:
                    context = context[-max_context:]
    return dags


def _left(box0, box1):
    if box0[3] <= box1[1] or box0[1] >= box1[3]:
        return False
    if 0 <= box1[0] - box0[2] <= 10:
        return True
    else:
        return False


def _top(box0, box1):
    if box0[2] <= box1[0] or box0[0] >= box1[2]:
        return False
    if 0 <= box1[1] - box0[3] <= 10:
        return True
    else:
        return False


def create_dag(block):
    horizontal = {}
    vertical = {}

    cells, texts = zip(*block)
    for i in range(len(cells)):
        for j in range(len(cells)):
            if _left(cells[i], cells[j]):
                if i not in horizontal:
                    horizontal[i] = []
                horizontal[i].append(j)
            elif _top(cells[i], cells[j]):
                if i not in vertical:
                    vertical[i] = []
                vertical[i].append(j)

    return {
        'horizontal': horizontal,
        'vertical': vertical,
        'cells': list(cells),
        'texts': list(texts),
    }


def mask_to_spans(mask):
    last = 0
    result = []
    for i, current in enumerate(mask):
        if current > last:
            start = i
        elif current < last:
            result.append((start, i))
        last = current
    if current:
        result.append((start, len(mask)))
    return result


def spans_to_mask(spans, target, start=1, increment=0):
    for span in spans:
        target[span[0] : span[1]] = start
        start += increment


def mod_align(v, mod):
    return (v + mod - 1) // mod * mod


def get_segments(array):
    '''
    array: [False, True, True, True, False, True]
    segments: (1, 4), (5, 6)
    '''
    ruler = np.arange(len(array))
    array = np.concatenate([[False], array, [False]])
    starts = ruler[array[1:-1] & (~array[:-2])]
    ends = ruler[array[1:-1] & (~array[2:])] + 1
    return zip(starts, ends)


def line_sorter(box_retriever):
    def sorter(a, b):
        a, b = box_retriever(a), box_retriever(b)
        vertical_overlap, _, reference, _ = overlap(a[1], a[3], b[1], b[3])
        if reference and vertical_overlap / reference <= 0.25:
            return (a[1] + a[3]) / 2 - (b[1] + b[3]) / 2
        else:
            return a[0] - b[0]

    return sorter


def cell_sorter(box_retriever):
    def sorter(a, b):
        a, b = box_retriever(a), box_retriever(b)
        d = (a[1] + a[3]) / 2 - (b[1] + b[3]) / 2
        h = (a[3] - a[1] + b[3] - b[1]) / 2
        if abs(d / h) < 0.2:
            return a[0] - b[0]
        else:
            return d

    return sorter


def bubble_sort(values, cmp):
    for i in range(len(values)):
        for j in range(i + 1, len(values)):
            res = cmp(values[i], values[j])
            if res > 0:
                x = values[i]
                values[i] = values[j]
                values[j] = x
    return values


def bitmask_to_spans(mask):
    diff = mask[:-1] ^ mask[1:]  # start-1: -1, #end-1: 1
    anchors, *_ = np.where(diff)
    if anchors.size == 0:
        if mask[0]:
            return [(0, mask.size)]
        else:
            return []
    anchors += 1
    start = 0
    result = []
    for anchor in anchors:
        if mask[anchor]:
            start = anchor
        else:
            result.append((start, anchor))
            start = None
    if start is not None:
        result.append((start, mask.size))
    return result


def expand_regions(shape_or_masks, existences, region):
    if not isinstance(shape_or_masks[0], np.ndarray):
        masks = [np.zeros(x, dtype=np.bool_) for x in shape_or_masks]
    else:
        masks = shape_or_masks
    left = region[0], (region[1] + region[3]) / 2
    right = region[2], (region[1] + region[3]) / 2
    top = (region[0] + region[2]) / 2, region[1]
    bottom = (region[0] + region[2]) / 2, region[3]
    available = set()
    available.add(_expand_region(masks, existences, left, 2))
    available.add(_expand_region(masks, existences, right, 0))
    available.add(_expand_region(masks, existences, top, 3))
    available.add(_expand_region(masks, existences, bottom, 1))
    if None in available:
        available.remove(None)
    return available


def _expand_region(masks, existences, point, direction):
    def _compute_intersection(point, idx):
        point_shift = 1 - idx % 2
        axis_idx = idx
        for _region in existences:
            if _region[axis_idx] == point[1 - point_shift]:
                if _region[point_shift] < point[point_shift] < _region[2 + point_shift]:
                    return 1
        return 0

    def _line(point, axis_shift):
        mask = masks[axis_shift]
        mask.fill(True)
        for _region in existences:
            if _region[axis_shift] < point[axis_shift] < _region[2 + axis_shift]:
                mask[_region[1 - axis_shift] : _region[3 - axis_shift]] = False
        for span in bitmask_to_spans(mask):
            if span[0] <= point[1 - axis_shift] <= span[1]:
                return span
        else:
            return None

    def _expand_line(point, line, axis_shift):
        mask = masks[axis_shift]
        mask.fill(True)
        for _region in existences:
            ov, *_ = overlap(_region[axis_shift], _region[axis_shift + 2], *line)
            if ov > 0:
                mask[_region[1 - axis_shift] : _region[3 - axis_shift]] = False
        for span in bitmask_to_spans(mask):
            if span[0] <= point[1 - axis_shift] < span[1]:
                if axis_shift == 0:
                    return (line[0], span[0], line[1], span[1])
                else:
                    return (span[0], line[0], span[1], line[1])
        else:
            return None

    if _compute_intersection(point, direction):
        return None
    axis_shift = 1 - (direction & 1)
    line = _line(point, axis_shift)
    if line is None:
        return None
    region = _expand_line(point, line, 1 - axis_shift)
    return region


def _make_margin_regions(shape, margin):
    if isinstance(margin, abc.Sequence):
        if len(margin) == 2:
            top = bottom = margin[0]
            left = right = margin[1]
        else:
            top, bottom, left, right = margin
    else:
        left = right = top = bottom = margin
    region0 = 0, 0, left, shape[0]
    region1 = shape[1] - right, 0, shape[1], shape[0]
    region2 = left, 0, shape[1] - right, top
    region3 = left, shape[0] - bottom, shape[1] - right, shape[0]
    return [region0, region1, region2, region3]


def compute_availabe_regions(shape, existences):
    masks = [np.zeros(x, dtype=np.bool_) for x in shape]
    available = set()
    if not existences:
        available.add((0, 0, shape[1], shape[0]))
    else:
        for _region in existences:
            available |= expand_regions(masks, existences, _region)
    return available


def select_region(available, size, strategy):
    def _claim_region(available, size, strategy):
        candidates = [x for x in available if x[2] - x[0] >= size[1] and x[3] - x[1] >= size[0]]
        if not candidates:
            return None
        if strategy == 'compact':
            candidates.sort(key=lambda x: area(x))
            return candidates[0]
        else:
            return random.choice(candidates)

    select = _claim_region(available, size, strategy)
    if select is None:
        return None
    if strategy == 'compact':
        width, height = size[1], size[0]
        return (select[0], select[1], select[0] + width, select[1] + height)
    else:
        width_select, height_select = (
            select[2] - select[0],
            select[3] - select[1],
        )
        width_region, height_region = size[1], size[0]
        x = np.random.randint(0, width_select - width_region + 1) + select[0]
        y = np.random.randint(0, height_select - height_region + 1) + select[1]
        return (x, y, x + width_region, y + height_region)


def claim_region(shape, existences, size, strategy='compact'):
    available = compute_availabe_regions(shape, existences)
    return select_region(available, size, strategy)


def _clip_region(shape, region):
    x0, y0, x1, y1 = region
    x0, y0 = max(0, x0), max(0, y0)
    x1, y1 = min(shape[1], x1), min(shape[0], y1)
    x1, y1 = max(x0, x1), max(y0, y1)
    return x0, y0, x1, y1


class FastClaimRegion:
    def __init__(self, shape, existences=None, strategy='compact', margin=None):
        self.shape = shape
        self.masks = [np.zeros(x, dtype=np.bool_) for x in shape]
        self.existences = [_clip_region(shape, x) for x in existences or []]
        if margin is not None:
            self.existences += _make_margin_regions(shape, margin)
        self.available = compute_availabe_regions(shape, self.existences)
        self.strategy = strategy

    def __call__(self, size):
        region = select_region(self.available, size, self.strategy)
        if region is not None:
            self.__recompute_available(region)
        return region

    def can_claim(self, size):
        return np.any([x[2] - x[0] >= size[1] and x[3] - x[1] >= size[0] for x in self.available])

    def __recompute_available(self, region):
        self.existences.append(region)
        intersected_available = self.__remove_intersected_available(region)
        available = set()
        for point, direction in self.__collect_points(intersected_available):
            available.add(_expand_region(self.masks, self.existences, point, direction))
        available |= expand_regions(self.masks, self.existences, region)
        if None in available:
            available.remove(None)
        self.available |= available

    def __remove_intersected_available(self, region):
        intersected = set([x for x in self.available if iou(region, x) > 0])
        self.available -= intersected
        return intersected

    def __collect_points(self, available):
        for region in available:
            for _region in [
                x
                for x in self.existences
                if x[2] == region[0] or x[0] == region[2] or x[1] == region[3] or x[3] == region[1]
            ]:
                left = _region[0], (_region[1] + _region[3]) / 2
                right = _region[2], (_region[1] + _region[3]) / 2
                top = (_region[0] + _region[2]) / 2, _region[1]
                bottom = (_region[0] + _region[2]) / 2, _region[3]
                if region[1] < left[1] < region[3]:
                    yield left, 2
                if region[1] < right[1] < region[3]:
                    yield right, 0
                if region[0] < top[0] < region[2]:
                    yield top, 3
                if region[0] < bottom[0] < region[2]:
                    yield bottom, 1
