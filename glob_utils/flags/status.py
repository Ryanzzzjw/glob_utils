
################################################################################
# Custom flag
################################################################################
from abc import ABC, abstractmethod
from enum import Enum
from glob_utils.thread_process.signal import Signal


class BaseStatus(Enum):
    """"""

class StatusAgent(object):
    """Agent which allow manage a Status, which can take multiple values.
    
    e.g.:class Status(BaseStatus):
                IDLE = 1
                MEASURING = 1
                PAUSED = 1

    agent= StatusAgent(list(Status))

    The first value in the status_values list will be took as 
    initialisation value for the status.

    the signal 'changed' will be emitted when the status value is changed
    
    Args:
        status_values (list[Enum]): list of values which the 
        status can take.
    """
    _status:Enum # Actual status value
    _status_old:Enum # Last/older status value 
    _status_values:list[Enum] # list of values which the status can take
    changed: Signal # Signal is emited if the status value has been changed 

    def __init__(self, status_values:list[Enum]) -> None:
        super().__init__()
        self.changed= Signal(self)
        self._status_values = status_values
        self.reset()
        
    def change_status(self, val:Enum)->None:
        """Change the actual status value and memory the last value
        
        - memory older value
        - set new status value
        - emit changed signal

        Args:
            state (int): new status value

        Raises:
            ValueError: is raised if the value is not contained 
            in the _status_values list
        """
        if val not in self._status_values:
            raise ValueError(f'state should have the values {self._status_values}')
        self.set_old(self.actual_status())
        self._status=val
        if self.has_changed():
            self.changed.emit()
    
    def is_set(self, val:Enum)->bool:
        """Check if the actual status is set to val

        Args:
            val (Enum): status value to check

        Raises:
            ValueError: is raised if the value is not contained 
            in the _status_values list

        Returns:
            bool: return `True` if the actual status is set to val, 
            `False` otherwise
        """
        self._check_val(val)
        return self._status == val

    def actual_status(self)->Enum:
        """Return the actual status value

        Returns:
            Enum: value of actual status
        """
        return self._status

    def has_changed(self)->bool:
        """Asset if the status value changed since the last status change

        Returns:
            bool: `True` if the actual status differ from odler one,
            otherwise `False`
        """
        return self._status != self._status_old

    def reset(self, val:Enum=None)->None:
        """Reset both actual and last status values to the passed value

        Args:
            val (Enum, optional): reset status value. if set to `None`, 
            the first value in the _status_values list will be took as 
            initialisation value for the status. Defaults to `None`.

        Raises:
            ValueError: is raised if the value is not contained 
            in the _status_values list
        """
        if val is None:
            val= self._status_values[0]
        self._check_val(val)
        self._status_old = val
        self._status = val
        
    def set_old(self, val:Enum)->None:
        """Change the last/older status values

        Args:
            val (Enum): status value to set

        Raises:
            ValueError: is raised if the value is not contained 
            in the _status_values list
        """
        self._check_val(val)
        self._status_old = val
    
    def was_old(self, val:Enum)->bool:
        """Check if the status was set to val (check the last value of status)

        Args:
            val (Enum): status value to check

        Raises:
            ValueError: is raised if the value is not contained 
            in the _status_values list

        Returns:
            bool: return `True` if the last/older status was set to val, 
            `False` otherwise
        """
        self._check_val(val)
        return self._status_old == val
    
    def was_set(self)->Enum:
        """Return the last/older status

        Returns:
            Enum: last/older status
        """
        return self._status_old
    
    def _check_val(self, val:Enum)->None:
        """Check if the value is contained in the _status_values list
        Raises:
            ValueError: is raised if the value is not contained 
            in the _status_values list
        """
        if val not in self._status_values:
            raise ValueError(
                f'state should have the values {self._status_values}'
            )


class StatusNotInitializated(BaseException):
    """"""

class AddStatus(ABC):
    """This Class allow to add a status to exixting obj and provide 
    standard functionalities:

    - `set_status` -> set the status to a new val
    - `get_status` -> get actual status  
    - `is_status`  -> test if actual status is set to val
    - `reset_to_last_status` -> set the status to last (memorized) value
    
    the abs-method `status_has_changed` is called when the status 
    has been changed, and need to be defined in new instance. 

    """
    _status_agent: StatusAgent
        
    def __init__(self) -> None:
        super().__init__()
        
    def init_status(self, status_values:BaseStatus) -> None:
        """initialize the multistatus intern object

        Args:
            status_values (BaseStatus): 
            hier the first enum should be the initial one
        """
        l= list(status_values)
        self._status_agent = StatusAgent(l)
        self._status_agent.reset(l[0])
        self._status_agent.changed.connect(self._status_has_changed) 
    
    def _status_has_changed(self)->None:
        """Update the was life flag, called by status changed signal"""
        self.status_has_changed(self._status_agent.actual_status(), self._status_agent.was_set())

    @abstractmethod
    def status_has_changed(self, status:Enum, was_status:Enum)->None:
        """This method is called wenn the status has been changed.

        Implement here what has to be done wenn the status changed!!

        Args:
            status (Enum): actual status
            was_status (Enum): older status
        """
    
    def emit_status_changed(self):
        self._status_has_changed()

    def is_status(self, val:Enum)->bool:
        self._check_is_init()
        return self._status_agent.is_set(val)
    
    def get_status(self)->Enum:
        self._check_is_init()
        return self._status_agent.actual_status()
    
    def set_status(self, val:Enum)->None:
        self._check_is_init()
        self._status_agent.change_status(val)

    def reset_to_last_status(self)->None:
        self._check_is_init()
        self._status_agent.change_status(self._status_agent.was_set())
    
    def _check_is_init(self):
        if self._status_agent is None:
            raise StatusNotInitializated(
                'Please init the Status of the object before using it')


if __name__ == "__main__":
    """"""
    a= StatusAgent()

    class Status(BaseStatus):
        IDLE = 1
        MEASURING = 1
        PAUSED = 1


    