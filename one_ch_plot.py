# %%
import general.loadings as ld
import general.settings as st
import pandas as pd
import matplotlib.pyplot as plt
import analysis.plotter as pl

FS, PRE_STIMULI, POST_STIMULI, chs, stimuli = st.Settings().set_basic_params()
directory, date, file, scale = ld.Loadings().read_config()

PLOT_CH:int = 1
# %%
kwargs_signal, kwargs_stimuli, kwargs_baseline, _ = pl.Figure().set_plot_theme()
fig = plt.figure(dpi=900, figsize=(12, 2))

for i in range(len(stimuli)):
    data = pd.read_csv(f"{directory}/{date}/csv/{file}_{list(stimuli.keys())[i]}_ch{PLOT_CH}.csv", header=None)

    ax = fig.add_subplot(1, len(stimuli), i+1)

    ax.plot([0, 0], [-scale, scale], **kwargs_stimuli)
    ax.plot([-PRE_STIMULI, POST_STIMULI], [0, 0], **kwargs_baseline)
    ax.plot(data[0], data[1]*1e3, **kwargs_signal)

    ax.set_title(list(stimuli.keys())[i])
    ax.set_xlim([-PRE_STIMULI, POST_STIMULI])
    ax.set_ylim([-scale, scale])

    pl.Figure().delete_axes()

pl.Figure().set_scale_bars(ax, scale)

plt.savefig(f"{directory}/{date}/csv/{file}_ch{PLOT_CH}_{scale / 2}uV.png", bbox_inches="tight")
plt.close()

# %%
