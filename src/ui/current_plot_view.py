import random

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from src.model.model import Model


class CurrentPlotView(FigureCanvasQTAgg):

    def __init__(self, model: Model):
        self.model = model

        figure = Figure()
        self.axes = figure.add_subplot(111)
        super(CurrentPlotView, self).__init__(figure)

        n_data = len(self.model.tele_info_frames)
        self.xdata = list(range(n_data))
        self.ydata = [frame.instantaneous_intensity_in_a for frame in self.model.tele_info_frames]

    def create_ui(self):
        self.update_plot()

    def update_plot(self):
        # Drop off the first y element, append a new one.
        self.ydata = self.ydata[1:] + [random.randint(0, 10)]
        self.axes.cla()  # Clear the canvas.
        self.axes.plot(self.xdata, self.ydata, 'r')
        # Trigger the canvas to update and redraw.
        self.draw()
