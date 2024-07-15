import matplotlib.pyplot as plt
import general.loadings as ld

class Figure(ld.Logs):
    def _set_plot_theme(self):
        """Set the plot theme"""
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
        ch_positions = [3, 2, 1, 4, 5, 6]

        return kwargs_signal, kwargs_stimuli, kwargs_baseline, ch_positions

    def _delete_axes(self):
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

    def _set_scale_bars(self, ax, scale:float):
        """Set the scale bars"""
        self.scale = scale
        self.VSCALE = scale / 2  # in uV
        self.HSCALE = 0.2  # in s
        self.HSCALE_START = 0.5
        self.ax = ax

        kwargs_scale = {
            "color": "black",
            "linewidth": 4
        }

        # Vertical scale bar
        self.ax.plot([self.HSCALE_START + self.HSCALE, self.HSCALE_START+self.HSCALE], [-self.scale*0.9, -self.scale*0.9 + self.VSCALE], **kwargs_scale)
        # Horizontal scale bar
        self.ax.plot([self.HSCALE_START, self.HSCALE_START+self.HSCALE], [-self.scale*0.9, -self.scale*0.9], **kwargs_scale)

    def plot_waves(self, t:float, waves:float, PRE_STIMULI:float, POST_STIMULI:float, chs, directory:str, date:str, file:str, scale:float, STIM_NAME:str):
        """Plot the waves for all channels"""

        self.title("Plotting waves...", "cyan")

        self.waves = waves
        self.chs = chs
        self.t = t
        self.PRE_STIMULI = PRE_STIMULI
        self.POST_STIMULI = POST_STIMULI
        self.directory = directory
        self.date = date
        self.file = file
        self.scale = scale
        self.STIM_NAME = STIM_NAME

        ch_num = len(self.chs)

        kwargs_signal, kwargs_stimuli, kwargs_baseline, ch_positions = self._set_plot_theme()

        fig = plt.figure(dpi=900)
        for c in range(ch_num):
            ax = fig.add_subplot(2, 3, ch_positions[c])

            ax.plot([0, 0], [-self.scale, self.scale], **kwargs_stimuli)
            ax.plot([-self.PRE_STIMULI, self.POST_STIMULI], [0, 0], **kwargs_baseline)
            ax.plot(self.t, self.waves[c]*1e3, **kwargs_signal)

            ax.set_title(f"Ch {c+1}")
            ax.set_xlim([-self.PRE_STIMULI, self.POST_STIMULI])
            ax.set_ylim([-self.scale, self.scale])

            self._delete_axes()

        self._set_scale_bars(ax, self.scale)

        plt.savefig(f"{self.directory}/{self.date}/{self.file}_{self.STIM_NAME}_{self.scale / 2}uV.png")
        plt.close()