import json
import pandas as pd
from rich import print
from scipy.io import loadmat

class Loadings():
    def __init__(self):
        self.directory: str
        self.date: list[str]
        self.file: list[float]
        self.scale: float

    def read_config(self):
        """Return the path of working directory, date, and file name"""
        f = open('config.json')
        config = json.load(f)
        self.directory = config['directory']
        self.date = config['date']
        self.file = config['file']
        self.scale = config['scale']  # in mV
        return self.directory, self.date, self.file, self.scale
    
    def read_mat(self, file:str):
        """Read mat file and return dict"""
        data = loadmat(file)
        return data

class Logs():
    def title(self, text:str):
        """Lot title of process"""
        self.text = text
        print(f"[bold magenta]{self.text}[/bold magenta]")

    def channel(self, ch:int):
        """Log message while processing each channel"""
        self.ch = ch
        print(f"[blue]Processing ch {ch}...[/blue]")