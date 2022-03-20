

from asyncio.log import logger
from queue import Queue
from typing import Any, Tuple


class Buffer(Queue):
    """"""
    def get_oldest(self):
        return None if self.empty() else self.get_nowait()

    def clear(self):
        while not self.empty():
            self.get_nowait()

    def rm_last(self):
        tmp = Queue()
        while not self.empty():
            tmp.put_nowait(self.get_nowait())

        while not tmp.empty():
            last = tmp.get_nowait()
            if not tmp.empty():
                self.put_nowait(last)
        return last or None

class Buffer2(object):
    """Class to manage a FIFO queue with custom methods for use as a buffer"""

    def __init__(self, maxsize=None) -> None:
        self.buffer = Queue(maxsize=maxsize)

    def is_full(self):
        return self.buffer.full()

    def is_empty(self):
        return self.buffer.empty()

    def add(self, data):
        self.buffer.put(data)

    def get_oldest(self) -> Tuple[Any,None]:
        return None if self.buffer.empty() else self.buffer.get_nowait()

    def clear(self):
        while not self.buffer.empty():
            self.buffer.get_nowait()

    def rm_last(self) -> Tuple[Any,None]:
        tmp = Queue()
        while not self.buffer.empty():
            tmp.put_nowait(self.buffer.get_nowait())

        while not tmp.empty():
            last = tmp.get_nowait()
            if not tmp.empty():
                self.buffer.put_nowait(last)
        return last or None


class BufferList(object):
    """Class to manage a FIFO queue with custom methods for use as a buffer"""
    buffer:list

    def __init__(self) -> None:
        self.clear()

    def is_empty(self):
        return not bool(self.buffer)

    def add(self, data):
        # logger.debug(f'add data to buffer:{data}')
        self.buffer.append(data)

    def get_oldest(self) -> Tuple[Any,None]:
        """Return oldest element. Return None if Buffer empty"""
        return self.buffer[0] if self.buffer else None
    
    def pop_oldest(self)->Any:
        """Remove oldest element and return it. Return None if Buffer empty"""
        return self.buffer.pop(0) if self.buffer else None

    def clear(self):
        self.buffer = []

    def rm_last(self) -> Tuple[Any,None]:
        tmp = Queue()
        while not self.buffer.empty():
            tmp.put_nowait(self.buffer.get_nowait())

        while not tmp.empty():
            last = tmp.get_nowait()
            if not tmp.empty():
                self.buffer.put_nowait(last)
        return last or None