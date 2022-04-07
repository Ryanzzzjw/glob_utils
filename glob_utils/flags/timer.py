###############################################################################
# custum Timer
################################################################################
class CustomTimer(object):
    max_time:float=1.0
    time_stp:float=0.1
    cnt:int=0
    max_cnt:int

    def __init__(self, max_time:float=1.0, time_stp:float=0.1) -> None:
        super().__init__()
        self.set_max_time(max_time)
        self.set_time_stp(time_stp)
        self.reset()

    def increment(self)->bool:
        # print('cnt', self.cnt, self.max_cnt, self.step, self._is_done())
        if self._is_done():
            self.reset()
            return True
        else:
            self.cnt+=1
            return False
    
    def reset(self)->None:
        self.cnt=0

    def set_max_time(self, max_time:float=1.0)->None:
        self.max_time=max_time
        self.set_counter()  

    def set_time_stp(self, time_stp:float=0.1)->None:
        self.time_stp=time_stp  
        self.set_counter()  

    def _is_done(self)->bool:
        return self.max_cnt==self.cnt
    
    def is_rst(self)->bool:
        return bool(self.cnt)

    def set_counter(self):
        self.max_cnt= int(self.max_time/self.time_stp)