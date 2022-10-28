import logging

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from src.model.model import Model

logger = logging.getLogger(__name__)


class CurrentPlotView(FigureCanvasQTAgg):
    DEFAULT_NUM_OF_X_ELEMENTS = 50

    def __init__(self, model: Model):
        self.model = model

        figure = Figure()
        self.axes = figure.add_subplot(111)
        super(CurrentPlotView, self).__init__(figure)

        self.xdata = list(range(self.DEFAULT_NUM_OF_X_ELEMENTS))
        intensity_values = [frame.instantaneous_intensity_in_a for frame in self.model.tele_info_frames]
        self.ydata = intensity_values[:50]

    def create_ui(self):
        self.update_plot()

    def update_plot(self):
        logger.debug(f'Update plot: model contains {len(self.model.tele_info_frames)} frames')

        self.xdata = list(range(len(self.model.tele_info_frames)))
        self.ydata = [frame.instantaneous_intensity_in_a for frame in self.model.tele_info_frames]

        self.axes.cla()
        if self.xdata and self.ydata:
            self.axes.plot(self.xdata, self.ydata, 'r')
        self.draw()

        # import numpy as np
        # import matplotlib.mlab as mlab
        # import matplotlib.pyplot as plt
        #
        # x = [21, 22, 23, 4, 5, 6, 77, 8, 9, 10, 31, 32, 33, 34, 35, 36, 37, 18, 49, 50, 100]
        # num_bins = 5
        # n, bins, patches = plt.hist(x, num_bins, facecolor='blue', alpha=0.5)
        # plt.show()
