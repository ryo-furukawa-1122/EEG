import matplotlib.pyplot as plt

class Figure():
    def _set_plot_theme(self):
        """Set the plot theme"""
        plt.rcParams["font.size"] = 18
        plt.rcParams["axes.linewidth"] = 1.4
        
        kwargs_signal = {
            "color": "black",
            "linewidth": 2
        }
        kwargs_stimuli = {
            "color": "royalblue",
            "linewidth": 1
        }
        ch_positions = [3, 2, 1, 4, 5, 6]

        return kwargs_signal, kwargs_stimuli, ch_positions
    
    def plot_waves(self, t:float, waves:float, PRE_STIMULI:float, POST_STIMULI:float, chs, directory:str, date:str, file:str, scale:float):
        """Plot the waves for all channels"""
        self.waves = waves
        self.chs = chs
        self.t = t
        self.PRE_STIMULI = PRE_STIMULI
        self.POST_STIMULI = POST_STIMULI
        self.directory = directory
        self.date = date
        self.file = file
        self.scale = scale

        ch_num = len(self.chs)

        kwargs_signal, kwargs_stimuli, ch_positions = self._set_plot_theme()

        fig = plt.figure(dpi=900)
        for c in range(ch_num):
            ax = fig.add_subplot(2, 3, ch_positions[c])
            ax.plot([0, 0], [-self.scale, self.scale], **kwargs_stimuli)
            ax.plot(self.t, self.waves[c]*1e3, **kwargs_signal)
            ax.set_title(f"Ch {c+1}")
            ax.set_xlabel("Time (s)")
            ax.set_ylabel("Voltage (\u03bcV)")
            ax.set_xlim([-self.PRE_STIMULI, self.POST_STIMULI])
            ax.set_ylim([-self.scale, self.scale])
        
        plt.savefig(f"{self.directory}/{self.date}/{self.file}_waves.png")
        plt.close()