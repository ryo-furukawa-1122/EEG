import json
from rich import print
from scipy.io import loadmat


class Logs():
    def title(self, text:str, color:str):
        """Lot title of process"""
        self.text = text
        self.color = color
        print(f"[bold {self.color}]{self.text}[/bold {self.color}]")

    def channel(self, ch:int, color:str):
        """Log message while processing each channel"""
        self.ch = ch
        self.color = color
        print(f"[{self.color}]Processing ch {ch}...[/{self.color}]")

class Loadings(Logs):
    def __init__(self):
        self.directory: str
        self.date: list[str]
        self.file: list[float]
        self.scale: float

    def read_config(self):
        """Return the path of working directory, date, and file name"""

        Logs.title(self, "Reading configuration...", "magenta")

        f = open('config.json')
        config = json.load(f)
        self.directory = config['directory']
        self.date = config['date']
        self.file = config['file']
        self.scale = config['scale']  # in uV
        return self.directory, self.date, self.file, self.scale
    
    def read_mat(self, file:str):
        """Read mat file and return dict"""

        Logs.title(self, "Reading mat file...", "green")

        data = loadmat(file)
        return data