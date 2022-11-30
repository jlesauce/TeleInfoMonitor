import logging

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from teleinfomonitor.model.model import Model

logger = logging.getLogger(__name__)


class PowerUsagePlotView(FigureCanvasQTAgg):
    DEFAULT_NUM_OF_X_ELEMENTS = 50

    def __init__(self, model: Model):
        self.model = model

        figure = Figure()
        self.axes = figure.add_subplot(111)
        super(PowerUsagePlotView, self).__init__(figure)

        self.xdata = list(range(self.DEFAULT_NUM_OF_X_ELEMENTS))
        intensity_values = [frame.instantaneous_intensity_in_a for frame in self.model.tele_info_frames]
        self.ydata = intensity_values[:50]

    def update_plot(self):
        if len(self.model.tele_info_frames) > 0:
            logger.debug(f'Update plot: model contains {len(self.model.tele_info_frames)} frames')

        self.xdata = list(range(len(self.model.tele_info_frames)))
        self.ydata = [frame.instantaneous_intensity_in_a for frame in self.model.tele_info_frames]

        self.axes.cla()
        if self.xdata and self.ydata:
            self.axes.plot(self.xdata, self.ydata, 'r')
        self.draw()
