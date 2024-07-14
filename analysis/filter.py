import numpy as np
from scipy import signal

class Filter():
    def _filter_params(self, fs:float):
        """Return the filter parameters"""
        fp_low = 0.3
        fp_high = 100
        fs_low = 0.1
        fs_high = 120
        gpass = 3
        gstop = 20

        self.fs = fs
        fn = self.fs / 2
        wp = [fp_low / fn, fp_high / fn]
        ws = [fs_low / fn, fs_high / fn]
        return [wp, ws, gpass, gstop]

    def _bandpass_filter(self, wave, fs:float):
        """Return the bandpass filter"""
        self.fs = fs
        self.wave = wave
        
        params = self._filter_params(self.fs)
        N, Wn = signal.buttord(*params)
        b, a = signal.butter(N, Wn, "band")
        y = signal.filtfilt(b, a, wave)
        return y
    
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
        self.fs = fs
        n_chs, n_trials, _ = data.shape
        filtered_data = np.zeros_like(data)
        for trial in range(n_trials):
            for ch in range(n_chs):
                filtered_data[ch, trial, :] = self._bandpass_filter(data[ch, trial, :], self.fs)
        return filtered_data
