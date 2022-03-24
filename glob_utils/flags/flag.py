


################################################################################
# Custom flag
################################################################################
from glob_utils.thread_process.signal import Signal


class CustomFlag(object):
    """Class responsible of creating and handling a flag (set, clear, is_set)"""
    
    def __init__(self) -> None:
        super().__init__()
        self.reset()

    def set(self, val:bool=True):
        """Set the flag"""
        self._set_old()
        self.flag=val

    def set_edge_up(self):
        """Set the flag"""
        self._set_old(False)
        self.flag=True

    def clear(self):
        """clear the flag"""
        self._set_old()
        self.flag=False

    def is_set(self):
        """Return value of the flag"""
        return self.flag

    def has_changed(self):
        return self.flag!=self.flag_old

    def is_raising_edge(self):
        return self.has_changed() and self.is_set()

    def reset(self):
        self.flag_old:bool=False
        self.flag:bool=False

    def ack_change(self):
        self._set_old()

    def _set_old(self, val:bool=None):
        self.flag_old = val or bool(self.flag)


class CustomFlagwSignals(object):
    """Class responsible of creating and handling a flag (set, clear, is_set)
    integrate some custum made signals"""
    
    def __init__(self) -> None:
        super().__init__()
        self.reset()
        self.changed=Signal(self)
        self.raising_edge=Signal(self)
        self.falling_edge=Signal(self)

    def set(self, val:bool=True):
        """Set the flag"""
        self._set_old()
        self.flag=val
        self.fire_signals()

    def set_edge_up(self):
        """Set the flag"""
        self.flag=False
        self.set(True)

    def clear(self):
        """clear the flag"""
        self.set(False)
    
    def fire_signals(self):
        if self.has_changed():
            self.changed.fire()
        if self.is_falling_edge():
            self.falling_edge.fire()
        if self.is_raising_edge():
            self.raising_edge.fire()

    def is_set(self):
        """Return value of the flag"""
        return self.flag

    def has_changed(self):
        return self.flag!=self.flag_old

    def is_raising_edge(self):
        return self.has_changed() and self.is_set()
    
    def is_falling_edge(self):
        return self.has_changed() and not self.is_set()

    def reset(self):
        self.flag_old:bool=False
        self.flag:bool=False

    def ack_change(self):
        self._set_old()

    def _set_old(self, val:bool=None):
        self.flag_old = val or bool(self.flag)


#
        

if __name__ == "__main__":
    """"""

    


    