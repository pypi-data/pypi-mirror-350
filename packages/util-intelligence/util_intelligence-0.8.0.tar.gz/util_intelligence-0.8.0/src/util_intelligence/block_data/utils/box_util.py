def bounding_box(boxes):
    return [
        min(x[0] for x in boxes),
        min(x[1] for x in boxes),
        max(x[2] for x in boxes),
        max(x[3] for x in boxes),
    ]


def overlap(s0, e0, s1, e1):
    t = (e0 - s0) + (e1 - s1)
    o = min(e0, e1) - max(s0, s1)
    min_length = min(e0 - s0, e1 - s1)
    max_length = max(e0 - s0, e1 - s1)
    return o, t, min_length, max_length


def line_cmp(box0, box1) -> float:
    vertical_overlap, _, reference, _ = overlap(
        box0[1], box0[3], box1[1], box1[3]
    )
    if reference > 0 and vertical_overlap / reference <= 0.25:
        return (box0[1] + box0[3] - box1[1] - box1[3]) / 2
    else:
        return box0[0] - box1[0]


def cell_cmp(box0, box1) -> float:
    d = (box0[1] + box0[3]) / 2 - (box1[1] + box1[3]) / 2
    h = (box0[3] - box0[1] + box1[3] - box1[1]) / 2
    if abs(d / h) < 0.2:
        return box0[0] - box1[0]
    else:
        return d
