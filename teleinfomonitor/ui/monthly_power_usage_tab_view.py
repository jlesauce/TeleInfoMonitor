import logging
from datetime import datetime

from PyQt6.QtCore import QDate
from observable import Observable

from teleinfomonitor.model.model import Model
from teleinfomonitor.ui.power_usage_plot_view import PowerUsagePlotView

logger = logging.getLogger(__name__)


class MonthlyPowerUsageTabView:
    EVENT_ID_ON_CALENDAR_DAY_SELECTED = 'calendar_day_selected_event'

    def __init__(self, parent_window, model: Model, listeners: Observable):
        self.parent = parent_window
        self.model = model
        self.listeners = listeners
        self.day_power_usage_plot_view = PowerUsagePlotView(self.model.tele_info_frames)

        self._init_ui()

    def _init_ui(self):
        self.parent.day_power_usage_layout.addWidget(self.day_power_usage_plot_view)
        self._init_calendar_widget_actions()

    # noinspection PyUnresolvedReferences
    def _init_calendar_widget_actions(self):
        self.parent.calendar_widget.clicked.connect(self._on_day_selector_clicked)

    def _on_day_selector_clicked(self):
        q_date: QDate = self.parent.calendar_widget.selectedDate()
        date_time = datetime.fromisoformat(str(q_date.toPyDate()))
        logger.debug(f'Notify day selected: {q_date.toPyDate()}')
        self.listeners.trigger(self.EVENT_ID_ON_CALENDAR_DAY_SELECTED, date_time.date())
