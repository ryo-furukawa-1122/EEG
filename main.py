# %%
import general.loadings as ld
import general.settings as st
import analysis.waveform as wv
import analysis.filter as fl
import analysis.plotter as pl
import analysis.spectrogram as sp
import numpy as np

E_NAME = "EVT01"
STIM_NAME = "2 kHz"
ld.Loadings().title(STIM_NAME, "blue")
FS, PRE_STIMULI, POST_STIMULI, chs, stimuli = st.Settings().set_basic_params()
directory, date, file, scale = ld.Loadings().read_config()
data = ld.Loadings().read_mat(f'{directory}/{date}/{file}.mat')

t = np.arange(-PRE_STIMULI, POST_STIMULI, 1/FS)
stim_number = stimuli[STIM_NAME]
lag = data[f"FP{chs[0]:02}_ts"][0, 0]
lag_sample = int(lag * FS)

stim_times = data[E_NAME][stim_number::5][:, 0] - lag
stim_stamp = np.array([int((stim_time) * FS) for stim_time in stim_times])

# %%
signals = wv.Waveform().arange_data(data, chs, stim_stamp, FS, PRE_STIMULI, POST_STIMULI)

# %%
filtered_signals = fl.Filter().filter_signals(signals, FS)
averaged_signals = wv.Waveform().averaged_wave(filtered_signals)

# %%
pl.Figure().plot_waves(t, averaged_signals, PRE_STIMULI, POST_STIMULI, directory, date, file, scale, STIM_NAME)

# %%
# sp.TimeFrequencyAnalyzer(FS).plot_time_frequency(t, averaged_signals, PRE_STIMULI, POST_STIMULI, directory, date, file, scale, STIM_NAME)