from abc import ABC
from PyQt6.QtWidgets import QMainWindow, QTabWidget
from ..database.db import SimulationModel, MonitorModel
from ..database.handler import DatabaseHandler


class TopLevel(QMainWindow):
    tabs: QTabWidget
    callback_delay: int = 10  # ms
    selected_simulation: SimulationModel
    selected_monitor: MonitorModel
    db_handler: DatabaseHandler

