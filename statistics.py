import numpy as np
from PyQt5.QtCore import pyqtSignal
import matplotlib.pyplot as plt
class Statistics():

    signal_plot = pyqtSignal()
    def __init__(self,episodes_batch_size,signal):
        """
        episodes_batch_size z ilu ostatnich epizoodów wyciągamy średnią

        """
        self.episodes_batch_size=episodes_batch_size

        self.score_list=[]
        self.last_score_batch=[]
        self.batches_means=[]
        self.signal_plot=signal


    def append_score(self,score):
        self.score_list.append(score)
        self.last_score_batch.append(score)
        if (self.score_list.__len__()-1)%self.episodes_batch_size==0:
            self.last_score_batch_table=np.asarray(self.last_score_batch)
            mean_from_batch=self.last_score_batch_table.mean()
            self.batches_means.append(mean_from_batch)
            self.last_score_batch=[]
            plt.plot(np.arange(self.batches_means.__len__()), self.batches_means)
            plt.savefig('new_curve.png')
            self.signal_plot.emit()







