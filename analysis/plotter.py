import matplotlib.pyplot as plt
import general.loadings as ld
import pandas as pd

class Figure(ld.Logs):
    def __init__(self):
        self.EXPORT_CH:int = 6
    
    def set_plot_theme(self):
        """Set the plot theme"""
        plt.rcParams["font.family"] = "Arial"
        plt.rcParams["font.size"] = 16
        plt.rcParams["axes.linewidth"] = 1.4
        
        kwargs_signal = {
            "color": "black",
            "linewidth": 2
        }
        kwargs_stimuli = {
            "color": "royalblue",
            "linewidth": 1
        }
        kwargs_baseline = {
            "color": "gray",
            "linewidth": 1,
            "linestyle": "dotted"
        }
        ch_positions = [5, 3, 1, 8, 7, 6]

        return kwargs_signal, kwargs_stimuli, kwargs_baseline, ch_positions

    def delete_axes(self):
        """Delete the axes and spines"""
        plt.tick_params(labelbottom=False,
                        labelleft=False,
                        labelright=False,
                        labeltop=False)
        plt.tick_params(bottom=False,
                        left=False,
                        right=False,
                        top=False)
        plt.gca().spines['right'].set_visible(False)
        plt.gca().spines['left'].set_visible(False)
        plt.gca().spines['top'].set_visible(False)
        plt.gca().spines['bottom'].set_visible(False)

    def _save_csv(self, t:float, wave:float, ch:int):
        """Save the data in a csv file"""
        self.ch = ch
        data = {
            "Time": t,
            "Wave": wave
        }
        df = pd.DataFrame(data)
        df.to_csv(f"{self.directory}/{self.date}/csv/{self.file}_ch{self.ch}_{self.STIM_NAME}.csv", index=False, header=False)

    def set_scale_bars(self, ax, scale:float):
        """Set the scale bars"""
        self.scale = scale
        self.VSCALE = scale / 2  # in uV
        # self.HSCALE = 0.2  # in s
        # self.HSCALE_START = 0.5
        self.HSCALE = 0.1  # in s
        self.HSCALE_START = 0.15
        self.ax = ax

        kwargs_scale = {
            "color": "black",
            "linewidth": 4
        }

        # Vertical scale bar
        self.ax.plot([self.HSCALE_START + self.HSCALE, self.HSCALE_START+self.HSCALE], [-self.scale*0.9, -self.scale*0.9 + self.VSCALE], **kwargs_scale)
        # Horizontal scale bar
        self.ax.plot([self.HSCALE_START, self.HSCALE_START+self.HSCALE], [-self.scale*0.9, -self.scale*0.9], **kwargs_scale)

    def plot_waves(self, t:float, waves:float, PRE_STIMULI:float, POST_STIMULI:float, directory:str, date:str, file:str, scale:float, STIM_NAME:str):
        """Plot the waves for all channels"""

        self.title("Plotting waves...", "cyan")

        self.waves = waves
        self.t = t
        self.PRE_STIMULI = PRE_STIMULI
        self.POST_STIMULI = POST_STIMULI
        self.directory = directory
        self.date = date
        self.file = file
        self.scale = scale
        self.STIM_NAME = STIM_NAME

        kwargs_signal, kwargs_stimuli, kwargs_baseline, ch_positions = self.set_plot_theme()

        ch_num = len(ch_positions)

        fig = plt.figure(dpi=900)
        for c in range(ch_num):
            ax = fig.add_subplot(2, 3, c+1)

            ax.plot([0, 0], [-self.scale, self.scale], **kwargs_stimuli)
            ax.plot([-self.PRE_STIMULI, self.POST_STIMULI], [0, 0], **kwargs_baseline)
            ax.plot(self.t, self.waves[ch_positions[c]-1]*1e3, **kwargs_signal)

            ax.set_title(f"Ch {c+1}")
            ax.set_xlim([-self.PRE_STIMULI, self.POST_STIMULI])
            ax.set_ylim([-self.scale, self.scale])

            self.delete_axes()
            
            if c == self.EXPORT_CH-1:
                self._save_csv(self.t, self.waves[ch_positions[c]-1], self.EXPORT_CH)

        self.set_scale_bars(ax, self.scale)

        plt.savefig(f"{self.directory}/{self.date}/{self.file}_{self.STIM_NAME}_{self.scale / 2}uV.png", bbox_inches="tight")
        plt.close()

    def plot_two_waves(self, t:float, wave_pre:float, wave_post:float, PRE_STIMULI:float, POST_STIMULI:float, directory:str, date:str, file:str, scale:float, STIM_NAME:str):
        """Plot the waves for all channels"""

        self.title("Plotting waves...", "cyan")

        self.wave_pre = wave_pre
        self.wave_post = wave_post
        self.t = t
        self.PRE_STIMULI = PRE_STIMULI
        self.POST_STIMULI = POST_STIMULI
        self.directory = directory
        self.date = date
        self.file = file
        self.scale = scale
        self.STIM_NAME = STIM_NAME

        kwargs_signal, kwargs_stimuli, kwargs_baseline, ch_positions = self.set_plot_theme()

        ch_num = len(ch_positions)

        fig = plt.figure(dpi=900)
        for c in range(ch_num):
            ax = fig.add_subplot(2, 3, c+1)

            ax.plot([0, 0], [-self.scale, self.scale], **kwargs_stimuli)
            ax.plot([-self.PRE_STIMULI, self.POST_STIMULI], [0, 0], **kwargs_baseline)
            ax.plot(self.t, self.wave_pre[ch_positions[c]-1]*1e3, **kwargs_signal)
            ax.plot(self.t, self.wave_post[ch_positions[c]-1]*1e3, linewidth=2, color="#FC5185")

            ax.set_title(f"Ch {c+1}")
            ax.set_xlim([-self.PRE_STIMULI, self.POST_STIMULI])
            ax.set_ylim([-self.scale, self.scale])

            self.delete_axes()
            
        self.set_scale_bars(ax, self.scale)

        plt.savefig(f"{self.directory}/{self.date}/{self.file}_{self.STIM_NAME}_{self.scale / 2}uV_plasticity.png", bbox_inches="tight")
        plt.close()
