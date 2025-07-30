import base64
import os
import pickle
import random
import threading

import h5py  # type: ignore
import numpy as np


class hdlist(object):
    def __init__(self, path, cache_size=0, mode='w'):
        if mode == 'w':
            try:
                self._file = h5py.File(path, 'w')
            except Exception:
                raise Exception(f'unable to create hdfile {path}')
            dt = h5py.string_dtype()
            self._dset = self._file.create_dataset('data', (0,), maxshape=(None,), dtype=dt)
            self._imap = []
        else:
            self._file = h5py.File(path, 'r')
            self._dset = self._file['data']
            self._imap = list(range(self.__len__()))
        self._cache_size = cache_size
        self._cache = {}
        self._cache_position = 0
        self._cache_thread = None

    def close(self):
        self._file.close()

    def __len__(self):
        return len(self._dset)

    def append(self, record):
        index = self.__len__()
        self._dset.resize(index + 1, 0)
        self._dset[index] = __class__._encode(record)
        self._imap.append(index)

    def __iadd__(self, records):
        index = self.__len__()
        self._dset.resize(index + len(records), 0)
        for record in records:
            self._dset[index] = __class__._encode(record)
            self._imap.append(index)
            index += 1
        return self

    def __getitem__(self, key):
        if isinstance(key, slice):
            return [self.__getitem__(x) for x in range(key.start, key.stop, key.step or 1)]
        else:
            _key = self._imap[key]
            if self._cache_thread is None:
                if key < self._cache_position:
                    self._cache.clear()
                    self._cache_position = 0
                if key - self._cache_position >= len(self._cache) * 3 // 4:
                    self._activate_caching(key)
            return self._cache.get(_key, None) or __class__._decode(self._dset[_key])

    def __setitem__(self, key, record):
        self._dset[key] = __class__._encode(record)

    def __iter__(self):
        self._cur = 0
        return self

    def __next__(self):
        if self._cur < self.__len__():
            result = self.__getitem__(self._cur)
            self._cur += 1
            return result
        else:
            raise StopIteration()

    @staticmethod
    def _encode(data):
        return base64.b64encode(pickle.dumps(data))

    @staticmethod
    def _decode(data):
        return pickle.loads(base64.b64decode(data))

    def _activate_caching(self, position):
        if self._cache_size == 0 or self._cache_position + len(self._cache) >= self.__len__():
            return

        def bind(position):
            erasing = self._imap[self._cache_position : position]
            for _key in erasing:
                del self._cache[_key]
            self._cache_position = position
            while len(self._cache) < self._cache_size:
                position = self._cache_position + len(self._cache)
                if position >= len(self._imap):
                    break
                _key = self._imap[position]
                self._cache[_key] = __class__._decode(self._dset[_key])
            self._cache_thread = None

        self._cache_thread = threading.Thread(target=bind, args=(position,), daemon=True)
        self._cache_thread.start()

    def shuffle(self):
        random.shuffle(self._imap)


class rslist(object):
    def __init__(self, path, slice_size=100, num_slices=10, cache_size=None):
        chunk_size = 1024**2
        cache_size = cache_size or 0
        self._file = h5py.File(
            path,
            'r',
            rdcc_nbytes=chunk_size,
            rdcc_nslots=cache_size // chunk_size,
        )
        self._dset = self._file['data']
        self._cache = []
        self._slice_size = slice_size
        self._num_slices = num_slices
        if self.__len__() < slice_size:
            raise Exception(
                f'data size {self.__len__()} in {path} is smaller than slice size {slice_size}'
            )

    def close(self):
        self._file._close()

    def __len__(self):
        return len(self._dset)

    def get(self, size):
        while size > len(self._cache):
            for _ in range(self._num_slices):
                self._load_data(self._slice_size)
        data = self._retrieve(size)
        return data

    def _load_data(self, size):
        index = np.random.randint(0, self.__len__() - size + 1)
        data = self._dset[index : index + size]
        self._cache += list(data)
        np.random.shuffle(self._cache)

    def _retrieve(self, size):
        data = self._cache[:size]
        self._cache = self._cache[size:]
        return data


class shelvedict(object):
    def __init__(self, path, flag='r'):
        import shelve

        self._dset = shelve.open(os.path.join(path, 'dset'), flag=flag)

    def __getitem__(self, key):
        return self._dset[key]

    def __setitem__(self, key, record):
        self._dset[key] = record

    def __len__(self):
        return len(self._dset)

    def todict(self):
        return dict(self._dset)


if __name__ == '__main__':
    hdl = hdlist('test.h5', 10)
    import time

    for k in range(100):
        hdl.append(k)
    hdl.shuffle()
    for k in range(100):
        print(hdl[k])
        time.sleep(0.01)
    hdl += [3, 4]
    hdl.close()
    print(hdl[3:6])
    print('done')
