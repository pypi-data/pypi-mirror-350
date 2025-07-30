import threading
import time

import numpy as np

from . import context


def run_async(target, args=tuple(), inheritate_context=tuple(), callback=None):
    inheritate_context_store = {
        k: getattr(context, k).storage for k in inheritate_context
    }

    def bind():
        for k, v in inheritate_context_store.items():
            getattr(context, k).storage.update(v)
        try:
            target(*args)
        finally:
            context.local.release()

    def daemon(t):
        t.join()
        if callable(callback):
            callback()

    thread = threading.Thread(target=bind, daemon=callback is not None)
    thread.start()
    if callback is not None:
        daemon_thread = threading.Thread(target=daemon, args=(thread,))
        daemon_thread.start()
    return thread


class DataProducer:
    def __init__(self, minsize, maxsize):
        self.queue = []
        self.lock = threading.Lock()
        self.minsize = minsize
        self.maxsize = maxsize

    def start(self, thread_num=1):
        for _ in range(thread_num):
            run_async(self._worker)

    def _worker(self):
        while True:
            if self.size >= self.maxsize:
                time.sleep(1)
                continue
            self._produce()

    def _produce(self):
        raise NotImplementedError()

    @property
    def size(self):
        return len(self.queue)

    def get(self, size):
        while self.size < self.minsize:
            time.sleep(0.1)
        self.lock.acquire()
        indices = np.random.choice(self.size, size, replace=False)
        records = [self.queue[x] for x in indices]
        if self.size >= self.maxsize:
            self.queue = [
                self.queue[x] for x in range(self.size) if x not in indices
            ]
        self.lock.release()
        return records

    def put(self, records):
        self.lock.acquire()
        self.queue += records
        self.lock.release()
