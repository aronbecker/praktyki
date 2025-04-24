from PyQt5.QtWidgets import (QWidget, QStackedWidget, QVBoxLayout,)
from ShowTournaments import ShowTournamentsWindow
from RoundsWindow import RoundsPage
from TablesWindow import TablesWindow
from Turniej import Turniej
class TournamentWidget(QWidget):
    def __init__(self, turnieje):
        super().__init__()
        self.turnieje = turnieje
        self.layout = QVBoxLayout(self)
        self.stacked_widget = QStackedWidget(self)

        # Add pages to the stacked widget
        self.show_tournaments_page = ShowTournamentsPage(self.turnieje)
        self.rounds_window = RoundsPage(self.turnieje)
        self.tables_window = TablesWindow()

        self.stacked_widget.addWidget(self.show_tournaments_page)
        self.stacked_widget.addWidget(self.rounds_window)
        self.stacked_widget.addWidget(self.tables_window)

        # Add the stacked widget to the layout
        self.layout.addWidget(self.stacked_widget)
        self.setLayout(self.layout)
