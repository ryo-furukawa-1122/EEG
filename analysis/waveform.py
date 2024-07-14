import numpy as np

class Waveform():
    def arange_data(self, data:dict, chs:list[int], stim_stamp:np.ndarray, FS:int, PRE_STIMULI:float, POST_STIMULI:float):
        """Arrange the data according to the event timings"""
        self.data = data
        self.chs = chs
        self.stim_stamp = stim_stamp
        self.FS = FS
        self.PRE_STIMULI = PRE_STIMULI
        self.POST_STIMULI = POST_STIMULI
        
        signals = []
        for ch in self.chs:
            wave = self.data[f"WB{ch:02}"]
            aranged_wave = []
            for stamp in self.stim_stamp:
                start_index = int(stamp - int(self.PRE_STIMULI*self.FS))
                end_index = int(stamp + int(self.POST_STIMULI*self.FS))
                wave_trim = wave[start_index:end_index]
                aranged_wave.append(wave_trim)
            signals.append(aranged_wave)
        signals = np.array(signals)[:, :, :, 0]
        return signals