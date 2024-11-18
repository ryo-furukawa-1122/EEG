# %%
import general.loadings as ld
import general.settings as st
import analysis.waveform as wv
import analysis.filter as fl
import analysis.plotter as pl
import analysis.spectrogram as sp
import numpy as np

E_NAME = "EVT01"
STIM_NAME = "4 kHz"
ld.Loadings().title(STIM_NAME, "blue")
FS, PRE_STIMULI, POST_STIMULI, chs, stimuli = st.Settings().set_basic_params()
directory, date, file, scale = ld.Loadings().read_config()
data_pre = ld.Loadings().read_mat(f'{directory}/{date}/{date}_pre.mat')
data_post = ld.Loadings().read_mat(f'{directory}/{date}/{date}_post.mat')

t = np.arange(-PRE_STIMULI, POST_STIMULI, 1/FS)
stim_number = stimuli[STIM_NAME]

lag_pre = data_pre[f"FP{chs[0]:02}_ts"][0, 0]
lag_sample_pre = int(lag_pre * FS)

lag_post = data_pre[f"FP{chs[0]:02}_ts"][0, 0]
lag_sample_post = int(lag_post * FS)

stim_times_pre = data_pre[E_NAME][stim_number::1][:, 0] - lag_pre
stim_stamp_pre = np.array([int((stim_time) * FS) for stim_time in stim_times_pre])

stim_times_post = data_post[E_NAME][stim_number::1][:, 0] - lag_post
stim_stamp_post = np.array([int((stim_time) * FS) for stim_time in stim_times_post])

# %%
signals_pre = wv.Waveform().arange_data(data_pre, chs, stim_stamp_pre, FS, PRE_STIMULI, POST_STIMULI)
signals_post = wv.Waveform().arange_data(data_post, chs, stim_stamp_post, FS, PRE_STIMULI, POST_STIMULI)

# %%
filtered_signals_pre = fl.Filter().filter_signals(signals_pre, FS)
averaged_signals_pre = wv.Waveform().averaged_wave(filtered_signals_pre)

filtered_signals_post = fl.Filter().filter_signals(signals_post, FS)
averaged_signals_post = wv.Waveform().averaged_wave(filtered_signals_post)

# %%
pl.Figure().plot_two_waves(t, averaged_signals_pre, averaged_signals_post, PRE_STIMULI, POST_STIMULI, directory, date, file, scale, STIM_NAME)

# %%
# sp.TimeFrequencyAnalyzer(FS).plot_time_frequency(t, averaged_signals, PRE_STIMULI, POST_STIMULI, directory, date, file, scale, STIM_NAME)