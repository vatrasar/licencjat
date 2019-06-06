import numpy as np
from PyQt5.QtCore import pyqtSignal
import matplotlib.pyplot as plt
import numpy as np
from collections import deque
class Statistics():

    signal_plot = pyqtSignal()
    def __init__(self,episodes_batch_size,signal):
        """
        episodes_batch_size z ilu ostatnich epizoodów wyciągamy średnią

        """
        self.episodes_batch_size=episodes_batch_size

        self.score_list=deque(maxlen=episodes_batch_size)
        self.last_score_batch=[]
        self.batches_means=[]
        self.signal_plot=signal
        plt.close()


    def append_score(self,score):
        self.score_list.append(score)
        self.last_score_batch.append(score)
        if (self.score_list.__len__()-1)%self.episodes_batch_size==0:

            mean_from_batch=self.get_last_score_batch_mean_score()
            self.batches_means.append(mean_from_batch)
            self.last_score_batch=[]
            plt.plot(np.arange(self.batches_means.__len__()), self.batches_means)
            plt.savefig('new_curve.png')
            self.signal_plot.emit()

    def get_last_score_batch_mean_score(self):
        last_score_batch_table = np.asarray(self.last_score_batch)
        return last_score_batch_table.mean()

    def get_current_mean_score(self):
        if self.batches_means.__len__()!=0 and self.batches_means.__len__()!=1:
            return self.batches_means[-1]
        elif self.batches_means.__len__()==1:
            self.last_score_batch.append(self.batches_means[0])
            mean_from_batch = self.get_last_score_batch_mean_score()
            self.batches_means.append(mean_from_batch)
            return self.batches_means[-1]
        else:
            return -9999999

class StatisticsBaseline(Statistics):

    def __init__(self, episodes_batch_size, signal):
        super().__init__(episodes_batch_size, signal)
        self.last_plot_episode=0

    def append_score(self, score, current_episode_number=0):
        score=np.asarray(score)

        if score.size>self.episodes_batch_size and current_episode_number-self.last_plot_episode>self.episodes_batch_size:
            self.batches_means.append(score[-self.episodes_batch_size:-1].mean())
            self.last_plot_episode=current_episode_number
            plt.plot(np.arange(self.batches_means.__len__()), self.batches_means)
            plt.savefig('new_curve.png')
            self.signal_plot.emit()

    def append_a2c(self, score, current_episode_number=0):
        self.score_list.append(score)
        if current_episode_number%self.episodes_batch_size==0 and self.score_list.__len__()!=0:
            scores=np.asarray(self.score_list)
            self.batches_means.append(scores.mean())
            plt.plot(np.arange(self.batches_means.__len__()), self.batches_means)
            plt.savefig('new_curve.png')
            self.signal_plot.emit()





