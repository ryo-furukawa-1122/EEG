# %%
import general.loadings as ld
import general.settings as st
import pandas as pd
import matplotlib.pyplot as plt
import analysis.plotter as pl

FS, PRE_STIMULI, POST_STIMULI, chs, stimuli = st.Settings().set_basic_params()
directory, date, file, scale = ld.Loadings().read_config()
kwargs_signal, kwargs_stimuli, kwargs_baseline, _ = pl.Figure().set_plot_theme()

PLOT_CH:int = 4

data_pre = pd.read_csv(f"{directory}/{date}/csv/{date}_pre_ch{PLOT_CH}_4 kHz.csv", header=None)
data_post = pd.read_csv(f"{directory}/{date}/csv/{date}_post_ch{PLOT_CH}_4 kHz.csv", header=None)
# %%
fig = plt.figure(dpi=900)
plt.plot([0, 0], [-scale, scale], **kwargs_stimuli)
plt.plot([-PRE_STIMULI, POST_STIMULI], [0, 0], **kwargs_baseline)
plt.plot(data_pre[0], data_pre[1]*1e3, linewidth=4, color="black")
plt.plot(data_post[0], data_post[1]*1e3, linewidth=4, color="#FC5185")
plt.xlim([-PRE_STIMULI, POST_STIMULI])
plt.ylim([-scale, scale])
pl.Figure().delete_axes()
pl.Figure().set_scale_bars(plt.gca(), scale)

plt.savefig(f"{directory}/{date}/csv/{date}_ch{PLOT_CH}_4kHz_{scale/2}.png", bbox_inches="tight")
plt.close()
