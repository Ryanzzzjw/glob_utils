from typing import Callable



class Signal(object):
    """
    Signal class.
    """
    def __init__(self, sender= None):
        super().__init__()
        self.sender = sender
        self.listeners = []

    def connect(self, callback:Callable):
        """
        Connect a callback with this signal.
        """
        self.listeners.append(callback)

    def disconnect(self, callback:Callable):
        """
        Disconnect the given callback from this signal.
        """
        self.listeners.remove(callback)

    def fire(self, *args, send_sender:bool=False, **kwargs):
        """
        Fire this signal.
        """
        for listener in self.listeners:
            if send_sender:
                listener(sender=self.sender, *args, **kwargs)
            else:
                listener(*args, **kwargs)
                
    def emit(self, *args, **kwargs):
        """
        Emit this signal.
        """
        self.fire(*args, **kwargs)