from collections import defaultdict
from typing import Any, Callable, Dict, Iterable, List, Optional, Union


class DisjointSet:
    def __init__(self):
        self.parents = {}

    def get_root(self, id: int) -> int:
        if id not in self.parents:
            self.parents[id] = id
        if self.parents[id] != id:
            self.parents[id] = self.get_root(self.parents[id])
        return self.parents[id]

    def union(self, ids: Iterable[int]) -> None:
        parents = [self.get_root(id) for id in ids]
        parent_joint = min(parents)
        for parent in parents:
            self.parents[parent] = parent_joint

    def groups(self, ids: Optional[Union[int, Iterable[int]]] = None) -> Dict[int, List[int]]:
        _ids = []
        if ids is None:
            _ids = self.parents.keys()
        elif isinstance(ids, int):
            _ids = list(range(ids))
        result = defaultdict(lambda: [])
        for id in _ids:
            result[self.get_root(id)].append(id)
        return dict(result)


def bubble_sort(
    iterable: Iterable,
    cmp: Callable[[Any, Any], float] = lambda x, y: (x > y) - (x < y),
    key: Callable[[Any], Any] = lambda x: x,
    reverse=False,
):
    if not isinstance(iterable, list):
        iterable = list(iterable)
    for i in range(len(iterable)):
        for j in range(i + 1, len(iterable)):
            res = cmp(key(iterable[i]), key(iterable[j]))
            if (res > 0 and not reverse) or (res < 0 and reverse):
                iterable[i], iterable[j] = iterable[j], iterable[i]
    return iterable
