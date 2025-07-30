import time
from collections import defaultdict
from typing import Dict


class Timer:
    __TIMERS__: Dict = defaultdict(lambda: 0)
    __TOTAL__: Dict = defaultdict(lambda: 0)

    def __init__(self):
        self._time = time.time()

    def check(self, name=None, count=None, synchronize=False):
        if synchronize:
            import torch

            torch.cuda.synchronize()
        now = time.time()
        elapsed = now - self._time
        self._time = now
        if name is not None:
            Timer.__TIMERS__[name] += elapsed
            Timer.__TOTAL__[name] += count or 0
        return elapsed

    @staticmethod
    def print():
        for k, v in Timer.__TIMERS__.items():
            c = Timer.__TOTAL__[k]
            if c == 0:
                print(f'{k}: {v:>.2F}')
            else:
                print(f'{k}: {v:>.2F}/{c}={v / c}')
