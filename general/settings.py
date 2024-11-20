import numpy as np

class Settings():
    def __init__(self):
        self.FS: int
        self.PRE_STIMULI: float
        self.POST_STIMULI: float
        self.chs: np.ndarray
        self.stimuli: dict

    def set_basic_params(self):
        """Return the basic parameters"""
        self.FS = 1e3
        self.PRE_STIMULI = 0.05  # in s
        self.POST_STIMULI = 0.3  # in s
        self.chs = np.arange(1, 9)
        self.stimuli:dict = {
            "2 kHz": 0,
            "4 kHz": 1,
            "8 kHz": 2,
            "16 kHz": 3,
            "32 kHz": 4
        }
        return self.FS, self.PRE_STIMULI, self.POST_STIMULI, self.chs, self.stimuli
    
