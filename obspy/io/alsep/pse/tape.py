# -*- coding: utf-8 -*-
import numpy as np
from obspy.core.util import open_bytes_stream
from .define import SIZE_PSE_RECORD
from .record import PseRecord


class PseTape(object):

    def __init__(self):
        self._record = None
        self._handle = None
        self._handle_has_fileno = False

    def __iter__(self):
        return self

    def __next__(self):
        self._record = self.fromfile()
        if self._record.size < SIZE_PSE_RECORD:
            raise StopIteration()
        return PseRecord(self._record)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def open(self, file):
        self._handle = open_bytes_stream(file)
        try:
            # see self.fromfile
            self._handle.fileno()
            self._handle_has_fileno = True
        except Exception:
            self._handle_has_fileno = False
        return self

    def close(self):
        self._handle.close()

    def fromfile(self):
        # np.fromfile accepts file path on-disk file-like
        # objects. In all other cases, use np.frombuffer:
        if not self._handle_has_fileno:
            buffer = self._handle.read(SIZE_PSE_RECORD)
            ret = np.frombuffer(buffer, dtype=np.uint8)
            # assert len(ret) == SIZE_PSE_RECORD
            return ret
        return np.fromfile(self._handle, dtype=np.uint8,
                           count=SIZE_PSE_RECORD)
