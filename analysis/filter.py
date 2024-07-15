import numpy as np
from scipy import signal
import general.loadings as ld

class Filter(ld.Logs):
    def _shift_data(self, data):
        """Return the shifted data"""
        n_chs, n_trials, _ = data.shape
        shifted_data = np.zeros_like(data)
        for trial in range(n_trials):
            for ch in range(n_chs):
                shifted_data[ch, trial, :] = data[ch, trial, :] - np.mean(data[ch, trial, :])
        return shifted_data

    def _filter_params(self, fs:float):
        """Return the filter parameters"""
        f_pass = 150
        f_stop = 100
        g_pass = 1
        g_stop = 20

        self.fs = fs

        fn = self.fs / 2
        wp = f_pass / fn
        ws = f_stop / fn
        return [wp, ws, g_pass, g_stop]

    def _lowpass_filter(self, wave, fs:float):
        """Return the lowpass filter"""
        self.fs = fs
        params = self._filter_params(self.fs)
        N, Wn = signal.buttord(*params)
        b, a = signal.butter(N, Wn, "low")
        y = signal.filtfilt(b, a, wave)
        return y
    
    def filter_signals(self, data, fs:float):
        """Return the filtered signals"""

        self.title("Filtering signals...", "yellow")

        self.fs = fs
        n_chs, n_trials, _ = data.shape
        filtered_data = np.zeros_like(data)
        unbiased_data = self._shift_data(data)
        for ch in range(n_chs):
            self.channel(ch, "gold")
            for trial in range(n_trials):
                filtered_data[ch, trial, :] = self._lowpass_filter(unbiased_data[ch, trial, :], self.fs)
        return filtered_data
