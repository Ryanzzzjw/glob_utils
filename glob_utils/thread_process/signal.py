class Signal(object):
    """
    Signal class.
    """
    def __init__(self, sender):
        super().__init__()
        self.sender = sender
        self.listeners = []

    def connect(self, callback):
        """
        Connect a callback with this signal.
        """
        self.listeners.append(callback)

    def disconnect(self, callback):
        """
        Disconnect the given callback from this signal.
        """
        self.listeners.remove(callback)

    def fire(self, send_sender=None, *args, **kwargs):
        """
        Fire this signal.
        """
        for listener in self.listeners:
            if send_sender:
                listener(sender=self.sender, *args, **kwargs)
            else:
                listener(*args, **kwargs)