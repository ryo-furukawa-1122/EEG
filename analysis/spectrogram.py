import general.loadings as ld
import matplotlib.pyplot as plt
from scipy.signal import spectrogram
import numpy as np

class TimeFrequencyAnalyzer(ld.Logs):
    def __init__(self, FS:float):
        self.FS = FS
    
    def _set_plot_theme(self):
        """Set the plot theme"""
        plt.rcParams["font.family"] = "Arial"
        plt.rcParams["font.size"] = 24
        plt.rcParams["axes.linewidth"] = 1.4
        
        kwargs_signal = {
            "color": "black",
            "linewidth": 2
        }
        kwargs_stimuli = {
            "color": "royalblue",
            "linewidth": 1
        }
        kwargs_baseline = {
            "color": "gray",
            "linewidth": 1,
            "linestyle": "dotted"
        }
        ch_positions = [5, 3, 1, 8, 7, 6]

        return kwargs_signal, kwargs_stimuli, kwargs_baseline, ch_positions
    
    def _compute_time_frequency(self, signal:float):
        """Compute the time-frequency analysis"""
        self.signal = signal
        
        self.title("Computing time-frequency analysis...", "green")
        
        f, t, Sxx = spectrogram(self.signal, self.FS, nperseg=256, noverlap=200)
        return f, t, Sxx
    
    def plot_time_frequency(self, time:float, waves:float, PRE_STIMULI:float, POST_STIMULI:float, directory:str, date:str, file:str, scale:float, STIM_NAME:str):
        """Plot the time-frequency analysis"""
        
        self.title("Plotting time-frequency analysis...", "green")

        self.waves = waves
        self.time = time
        self.PRE_STIMULI = PRE_STIMULI
        self.POST_STIMULI = POST_STIMULI
        self.directory = directory
        self.date = date
        self.file = file
        self.scale = scale
        self.STIM_NAME = STIM_NAME
        
        kwargs_signal, kwargs_stimuli, kwargs_baseline, ch_positions = self._set_plot_theme()
        
        ch_num = len(ch_positions)
        for c in range(ch_num):
            f, t, Sxx = self._compute_time_frequency(self.waves[ch_positions[c]-1]*1e6)
            
            fig, ax = plt.subplots(dpi=900)

            # pcm = ax.pcolormesh(t-self.PRE_STIMULI, f, 10*np.log10(Sxx), cmap="jet", vmin=0)
            im = ax.imshow(10*np.log10(Sxx), cmap="jet", extent=[t[0]-self.PRE_STIMULI, t[-1]-self.PRE_STIMULI, f[0], f[-1]], aspect="auto", vmax=-30)

            ax.set_ylabel('Frequency (Hz)')
            ax.set_xlabel('Time (s)')
            ax.set_ylim(0, 50)
            ax.set_xticks(np.arange(0, 0.8, 0.2))
            cbar = fig.colorbar(im)
            cbar.set_label('Power/Frequency (dB/Hz)', rotation=270, labelpad=18)
            
            plt.savefig(f"{self.directory}/{self.date}/{self.file}_{self.STIM_NAME}_ch{c+1}.png", bbox_inches="tight")
            plt.close()