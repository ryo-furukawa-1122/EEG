# %%
import json
import matplotlib.pyplot as plt
import glob
import numpy as np
from natsort import natsorted
import pandas as pd
from scipy import stats as st

plt.rcParams["font.family"] = "Arial"
plt.rcParams["font.size"] = 16
plt.rcParams["axes.linewidth"] = 1.4

f = open("config.json")
config = json.load(f)
directory = config["directory"]
ids = config["analysis_ids"]
f.close()

# %%
STIMULI:list[int] = [2, 4, 8, 16, 32]
FS:float = 1e3
PRE_STIMULI:float = 0.2
POST_STIMULI:float = 0.5
N:int = len(ids)

amplitude:np.ndarray[float] = np.zeros([N, len(STIMULI), 2])

for i in range(N):
    csv_files = natsorted(glob.glob(f"{directory}/{ids[i]}/csv/*.csv"))
    for j in range(len(STIMULI)):
        data = pd.read_csv(csv_files[j], header=None)
        amplitude[i, j, 0] = np.max(np.abs(data[1][:int(FS*PRE_STIMULI)]))  # Baseline
        amplitude[i, j, 1] = np.max(np.abs(data[1][int(FS*PRE_STIMULI):int(FS*POST_STIMULI)]))  # Response

amplitude *= 1e3
# %%
color1 = '#FC5185'
color2 = '#3FC1C9'
kwargs = {
    "showmeans": True,
    "meanprops": {
        "markerfacecolor": color1,
        "marker": "s",
        "markersize": 5,
        "markeredgecolor": "None"
    },
    "medianprops": {
        "color": color2,
        "linewidth": 1,
        "linestyle": "solid"
    },
    "widths": 0.5
}

fig = plt.figure(dpi=900, figsize=(12, 2))
for j in range(len(STIMULI)):
    ax = fig.add_subplot(1, len(STIMULI), j+1)
    ax.boxplot([amplitude[:, j, 0], amplitude[:, j, 1]], **kwargs)
    for i in range(N):
        ax.plot([1, 2], amplitude[i, j, :], linewidth=1, linestyle="dotted", color="#00000055")
    ax.set_xticklabels(["Pre", "Post"])
    ax.set_title(f"{STIMULI[j]} kHz")
    ax.set_ylim([0, 15])
    if j==0:
        ax.set_ylabel("Amplitude (\u03bcV)")
    
    # Wilcoxon signed-rank test
    _, p = st.wilcoxon(amplitude[:, j, 0], amplitude[:, j, 1], alternative="two-sided")
    print(f"Stimuli: {STIMULI[j]} kHz, p-value: {p:.3f}")

print("n = ", N)
plt.savefig(f"{directory}/Amplitude/Amplitude.png", bbox_inches="tight")
plt.close()
# %%

