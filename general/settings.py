import numpy as np
import matplotlib.pyplot as plt

class Settings():
    def set_basic_params(self):
        """Return the basic parameters"""
        FS = 40e3
        PRE_STIMULI = 0.2  # in s
        POST_STIMULI = 0.8  # in s
        chs = np.arange(9, 15)
        stimuli:dict = {
            "2 kHz": 0,
            "4 kHz": 1,
            "8 kHz": 2,
            "16 kHz": 3,
            "32 kHz": 4
        }
        return FS, PRE_STIMULI, POST_STIMULI, chs, stimuli
    
    def set_plot_theme(self):
        """Set the plot theme"""
        plt.rcParams["font.size"] = 18
        plt.rcParams["axes.linewidth"] = 1.4
        
        kwargs_signal = {
            "color": "black",
            "linewidth": 2
        }
        kwargs_stimuli = {
            "color": "royalblue",
            "linewidth": 1
        }
        return kwargs_signal, kwargs_stimuli
