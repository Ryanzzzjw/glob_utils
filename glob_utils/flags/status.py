
################################################################################
# Custom flag
################################################################################
from abc import ABC, abstractmethod
from enum import Enum
from glob_utils.thread_process.signal import Signal


class BaseStatus(Enum):
    """"""


class MultiState(object):
    """Create and handle a Status, which can take multiple value.
    """
    
    def __init__(self, status_values:list[Enum]) -> None:
        super().__init__()
        self.status_values = status_values
        self.reset()
        
    def change_state(self, state:int):
        """change the actual state"""
        if state not in self.status_values:
            raise ValueError(f'state should have the values {self.status_values}')
        self.set_old(self.state)
        self.state=state
    
    def is_set(self, state:int)->bool:
        """Return if actual state is set to value"""
        if state not in self.status_values:
            raise ValueError(f'state should have the values {self.status_values}')
        return self.state == state

    def actual_state(self):
        """Return value of the actual state"""
        return self.state

    def has_changed(self):
        return self.state != self.state_old

    def reset(self, state:int=None):
        self.state_old = state
        self.state = state

    def ack_change(self):
        self.set_old(self.state)
        
    def set_old(self, state:int):
        self.state_old = state
    
    def was_old(self, state:int)->bool:
        """Return if older state was set to value"""
        return self.state_old == state
    
    def was_set(self)->int:
        """Return the older state """
        return self.state_old


class MultiStatewSignal(MultiState):
    """Class responsible of creating and handling a flag (set, clear, is_set)"""
    
    def __init__(self,status_values:list[Enum]) -> None:
        super().__init__(status_values)
        self.changed= Signal(self)
    
    def change_state(self, state:Enum):
        """change the actual state"""
        if state not in self.status_values:
            raise ValueError(f'state should have the values {self.status_values}')
        self.set_old(self.actual_state())
        self.state=state
        self.fire_signals()
    
    def fire_signals(self):
        if self.has_changed():
            self.changed.fire()
            a= MultiStatewSignal()

class StatusNotInitializated(BaseException):
    """"""

class AddStatus(ABC):
    _status: MultiStatewSignal
    _was_status:Enum
    
        
    def __init__(self) -> None:
        super().__init__()
        

    def init_status(self, status_values:BaseStatus) -> None:
        """initialize the multistatus intern object

        Args:
            status_values (BaseStatus): 
            hier the first enum should be the initial one
        """
        l= list(status_values)
        self._status = MultiStatewSignal(l)
        self._status.reset(l[0])
        self._status.changed.connect(self._status_has_changed) 
    
    def _status_has_changed(self)->None:
        """Update the was life flag, called by status changed signal"""
        self.status_has_changed(self._status.actual_state(), self._status.was_set())

    @abstractmethod
    def status_has_changed(self, status:Enum, was_status:Enum)->None:
        """This method is called wenn the status has been changed.
        Implement here what has to be done wenn the status changed

        Args:
            status (_type_): actual status
            was_status (_type_): older status
        """
    def emit_status_changed(self):
        self._status_has_changed()

    def is_status(self, val:Enum)->bool:
        self._check_is_init()
        return self._status.is_set(val)
    
    def get_status(self)->Enum:
        self._check_is_init()
        return self._status.actual_state()
    
    def set_status(self, val:Enum)->None:
        self._check_is_init()
        self._status.change_state(val)

    def set_old_status(self)->None:
        self._check_is_init()
        self._status.change_state(self._status.was_set())
    
    def _check_is_init(self):
        if self._status is None:
            raise StatusNotInitializated(
                'Please init the Status of the object before using it')
   
class testS(AddStatus):

    def status_changed(self, status:Enum, was_status:Enum)-> None:
        """"""

if __name__ == "__main__":
    """"""

    class AStates(BaseStatus):
        IDLE = 1
        MEASURING = 1
        PAUSED = 1
    
    a=testS(AStates)


    