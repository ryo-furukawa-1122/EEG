# %%
import general.loadings as ld
import general.settings as st
import numpy as np
import analysis.waveform as wv
import analysis.filter as fl
import analysis.plotter as pl
import matplotlib.pyplot as plt

E_NAME = "EVT01"
STIM_NAME = "4 kHz"
PLOT_CH:int = 6

ld.Loadings().title(STIM_NAME, "blue")
FS, PRE_STIMULI, POST_STIMULI, chs, stimuli = st.Settings().set_basic_params()
directory, date, file, scale = ld.Loadings().read_config()
kwargs_signal, kwargs_stimuli, kwargs_baseline, _ = pl.Figure().set_plot_theme()

data_pre = ld.Loadings().read_mat(f'{directory}/{date}/{file}_pre.mat')
data_post = ld.Loadings().read_mat(f'{directory}/{date}/{file}_post.mat')

t = np.arange(-PRE_STIMULI, POST_STIMULI, 1/FS)
stim_number = stimuli[STIM_NAME]

lag_pre = data_pre[f"FP{chs[0]:02}_ts"][0, 0]
lag_sample_pre = int(lag_pre * FS)
lag_post = data_post[f"FP{chs[0]:02}_ts"][0, 0]
lag_sample_post = int(lag_post * FS)

stim_times_pre = data_pre[E_NAME][stim_number::1][:, 0] - lag_pre
stim_stamp_pre = np.array([int((stim_time) * FS) for stim_time in stim_times_pre])
stim_times_post = data_post[E_NAME][stim_number::1][:, 0] - lag_post
stim_stamp_post = np.array([int((stim_time) * FS) for stim_time in stim_times_post])

# %%
signals_pre = wv.Waveform().arange_data(data_pre, chs, stim_stamp_pre, FS, PRE_STIMULI, POST_STIMULI)
signals_post = wv.Waveform().arange_data(data_post, chs, stim_stamp_post, FS, PRE_STIMULI, POST_STIMULI)

filtered_signals_pre = fl.Filter().filter_signals(signals_pre, FS)
filtered_signals_post = fl.Filter().filter_signals(signals_post, FS)
# %%
_, kwargs_stimuli, kwargs_baseline, _ = pl.Figure().set_plot_theme()

kwargs_pre = {
    "linewidth": 4,
    "color": "black",
}
kwargs_post = {
    "linewidth": 4,
    "color": "#FC5185",
}
kwargs_trial_pre = {
    "linewidth": 1,
    "color": "black",
    "alpha": 0.25,
}
kwargs_trial_post = {
    "linewidth": 1,
    "color": "#FC5185",
    "alpha": 0.25,
}

fig = plt.figure(dpi=900)
plt.plot([0, 0], [-scale, scale], **kwargs_stimuli)
plt.plot([-PRE_STIMULI, POST_STIMULI], [0, 0], **kwargs_baseline)

for trial in range(filtered_signals_pre.shape[1]):
    plt.plot(t, filtered_signals_pre[PLOT_CH-1, trial, :] * 1e3, **kwargs_trial_pre)
    plt.plot(t, filtered_signals_post[PLOT_CH, trial, :] * 1e3, **kwargs_trial_post)

plt.plot(t, np.mean(filtered_signals_pre[PLOT_CH-1, :, :], axis=0) * 1e3, **kwargs_pre)
plt.plot(t, np.mean(filtered_signals_post[PLOT_CH-1, :, :], axis=0) * 1e3, **kwargs_post)

plt.xlim([-PRE_STIMULI, POST_STIMULI])
plt.ylim([-scale, scale])
pl.Figure().delete_axes()
pl.Figure().set_scale_bars(plt.gca(), scale)

plt.savefig(f"{directory}/{date}/csv/{date}_ch{PLOT_CH}_{STIM_NAME}_{scale/2}_trials.png", bbox_inches="tight")
plt.close()