import numpy as np


class Machine(object):
    def __init__(self, size_x, size_y=-1):
        if size_y == -1:
            size_y = size_x
        self.size_x, self.size_y = size_x, size_y
        #self.map = np.full((size_x, size_y), -1, dtype=np.int32)
        self.core_num = size_x * size_y

    def clear(self):
        pass
        #self.map = np.full((self.size_x, self.size_y), -1, dtype=np.int32)



