import logging

from observable import Observable

from teleinfomonitor.model.model import Model

logger = logging.getLogger(__name__)


class MonthlyPowerUsageTabView:

    def __init__(self, parent_window, model: Model, listeners: Observable):
        self.parent = parent_window
        self.model = model
        self.listeners = listeners

        self._init_ui()

    def _init_ui(self):
        self._init_calendar_widget_actions()

    # noinspection PyUnresolvedReferences
    def _init_calendar_widget_actions(self):
        self.parent.calendar_widget.clicked.connect(self._on_day_selector_clicked)

    def _on_day_selector_clicked(self):
        logger.debug(f'Day selected: {self.parent.calendar_widget.selectedDate()}')
