# %%
import general.loadings as ld
import general.settings as st
import analysis.waveform as wv
import analysis.filter as fl
import analysis.plotter as pl
import numpy as np

E_NAME = "EVT01"
FS, PRE_STIMULI, POST_STIMULI, chs, stimuli = st.Settings().set_basic_params()
# kwargs_signal, kwargs_stimuli, ch_positions = st.Settings().set_plot_theme()
directory, date, file, scale = ld.Loadings().read_config()
data = ld.Loadings().read_mat(f'{directory}/{date}/{file}.mat')

t = np.arange(-PRE_STIMULI, POST_STIMULI, 1/FS)
stim_number = stimuli["2 kHz"]
lag = data[f"WB{chs[0]:02}_ts"]
lag_sample = int(lag * FS)

stim_times = data[E_NAME][stim_number::5] - lag
stim_stamp = np.array([int((stim_time) * FS) for stim_time in stim_times])

# %%
signals = wv.Waveform().arange_data(data, chs, stim_stamp, FS, PRE_STIMULI, POST_STIMULI)

# %%
filtered_signals = fl.Filter().filter_signals(signals, FS)
averaged_signals = wv.Waveform().averaged_wave(filtered_signals)

# %%
pl.Figure().plot_waves(t, averaged_signals, PRE_STIMULI, POST_STIMULI, chs, directory, date, file, scale)
