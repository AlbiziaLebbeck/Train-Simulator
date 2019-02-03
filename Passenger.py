import numpy as np
from Settings import *

class Passenger():
    def __init__(self,id,railway):
        if railway:
            self.target = np.random.choice(range(id+1,no_station))
        else:
            self.target = np.random.choice(range(id))