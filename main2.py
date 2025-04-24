import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel,
    QMessageBox, QGraphicsDropShadowEffect, QGridLayout, QStackedWidget,
    QHBoxLayout
)
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt
from zawodnicy import Zawodnicy
from zawodnicy_gui2 import AddPlayerWindow, ShowPlayersWindow
from AddTournament import AddTournamentWindow
from RoundsWindow import RoundsWindow, SaveRoundWindow
from Turniej import Turniej
from Runda import Runda
from Table import Table
from ShowTournaments2 import ShowTournamentsWindow, RoundsWindow, TablesWindow

class TournamentManager(QWidget):
    def __init__(self):
        super().__init__()
        self.turnieje = Turniej(1, 2, 3, 4)
        self.zawodnicy = Zawodnicy()
        self.zawodnicy.create_table()
        self.setFocusPolicy(Qt.StrongFocus)
        self.init_ui()
        self.current_view_index = 0

    def init_ui(self):
        self.setWindowTitle("Menadżer Turniejów")
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #2691f7,
                    stop: 1 #e6f3ff
                );
            }
            QPushButton {
                background-color: rgba(255, 255, 255, 0.85);
                border: 1px solid #c0deff;
                border-radius: 18px;
                padding: 12px 24px;
                font-size: 17px;
                font-family: 'Segoe UI', sans-serif;
                color: #1a1a1a;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.95);
            }
            QPushButton:pressed {
                background-color: rgba(230, 244, 255, 0.95);
            }
        """)

        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(100, 100, 100, 100)
        self.main_layout.setSpacing(24)

        self.title_label = QLabel("🎯 Menadżer Turniejów")
        self.title_label.setFont(QFont("Segoe UI", 30, QFont.Bold))
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("color: #0a0a0a; background: transparent;")
        self.main_layout.addWidget(self.title_label)

        self.top_navigation_bar = QHBoxLayout() # Pasek nawigacyjny na górze
        self.main_layout.addLayout(self.top_navigation_bar)

        self.stacked_widget = QStackedWidget()  # Główny kontener do przełączania widoków
        self.main_layout.addWidget(self.stacked_widget)

        self.init_main_menu() # Inicjalizacja menu głównego

        self.setLayout(self.main_layout)
        self.setMinimumSize(1600, 1000)
        self.setFocus()

    def init_main_menu(self):
        self.main_menu_widget = QWidget()
        self.main_menu_layout = QVBoxLayout(self.main_menu_widget)
        self.main_menu_layout.setSpacing(20)

        def create_button(text, action):
            button = QPushButton(text)
            button.setMinimumHeight(52)
            shadow = QGraphicsDropShadowEffect()
            shadow.setBlurRadius(20)
            shadow.setOffset(0, 4)
            shadow.setColor(QColor(0, 0, 0, 40))
            button.setGraphicsEffect(shadow)
            button.clicked.connect(action)
            # Dodaj przycisk do paska nawigacyjnego, a nie do layoutu menu
            self.top_navigation_bar.addWidget(button)
            return button

        self.add_tournament_button = create_button("➕ Turniej", self.add_tournament)
        self.show_tournaments_button = create_button("📆 Turnieje", self.show_tournaments_view)
        self.add_player_button = create_button("🧍 Zawodnik", self.open_add_player)
        self.show_players_button = create_button("📑 Zawodnicy", self.open_show_players)

        self.stacked_widget.addWidget(self.main_menu_widget) # Dodaj główne menu do stacked widget
        self.current_view_index = self.stacked_widget.indexOf(self.main_menu_widget)

    def clear_stacked_widget(self):
        """Czyści wszystkie widżety ze stacked widget."""
        for i in range(self.stacked_widget.count()):
            widget = self.stacked_widget.widget(i)
            if widget:
                widget.deleteLater()

    def add_tournament(self):
        self.add_tournament_window = AddTournamentWindow()
        self.add_tournament_window.show()
        # Dodaj tymczasowy widok, aby stacked_widget miał co wyświetlić
        temp_widget = QWidget()
        temp_layout = QVBoxLayout(temp_widget)
        temp_label = QLabel("Dodaj Turniej")
        temp_layout.addWidget(temp_label)
        self.stacked_widget.addWidget(temp_widget)
        self.stacked_widget.setCurrentWidget(temp_widget)

    def show_tournaments_view(self):
        # Stwórz instancję ShowTournamentsWindow
        self.show_tournaments_window_inner = ShowTournamentsWindow(self.turnieje, self.stacked_widget)

        # Dodaj widżet ShowTournamentsWindow do stacked widget
        self.stacked_widget.addWidget(self.show_tournaments_window_inner)
        self.stacked_widget.setCurrentWidget(self.show_tournaments_window_inner)
        self.current_view_index = self.stacked_widget.indexOf(self.show_tournaments_window_inner)

        # Dodaj przycisk powrotu (opcjonalnie, jeśli chcesz powrót z poziomu tego widoku)
        back_button = QPushButton("Powrót do menu")
        back_button.clicked.connect(self.show_main_menu)
        self.show_tournaments_window_inner.layout().addWidget(back_button)

    def show_main_menu(self):
        """Wyświetla główne menu."""
        self.stacked_widget.setCurrentWidget(self.main_menu_widget)
        self.current_view_index = self.stacked_widget.indexOf(self.main_menu_widget)

    def open_add_player(self):
        self.add_player_window = AddPlayerWindow(self.zawodnicy, self.stacked_widget)
        self.stacked_widget.addWidget(self.add_player_window)
        self.stacked_widget.setCurrentWidget(self.add_player_window)
        # self.add_player_window.show()
        # Dodaj tymczasowy widok
        # temp_widget = QWidget()
        # temp_layout = QVBoxLayout(temp_widget)
        # temp_label = QLabel("Dodaj Zawodnika")
        # temp_layout.addWidget(temp_label)
        # self.stacked_widget.addWidget(temp_widget)
        # self.stacked_widget.setCurrentWidget(temp_widget)
        back_button = QPushButton("Powrót do menu")
        back_button.clicked.connect(self.show_main_menu)
        self.add_player_window.layout().addWidget(back_button)

    def open_show_players(self):
        self.show_players_window = ShowPlayersWindow(self.zawodnicy,  self.stacked_widget)
        self.stacked_widget.addWidget(self.show_players_window)
        self.stacked_widget.setCurrentWidget(self.show_players_window)
        self.current_view_index = self.stacked_widget.indexOf(self.show_players_window)
        # self.show_players_window.show()
        # Dodaj tymczasowy widok
        # temp_widget = QWidget()
        # temp_layout = QVBoxLayout(temp_widget)
        # temp_label = QLabel("Lista Zawodników")
        # temp_layout.addWidget(temp_label)
        # self.stacked_widget.addWidget(temp_widget)
        # self.stacked_widget.setCurrentWidget(temp_widget)
        back_button = QPushButton("Powrót do menu")
        back_button.clicked.connect(self.show_main_menu)
        self.show_players_window.layout().addWidget(back_button)

    def close_application(self):
        reply = QMessageBox.question(
            self,
            "Potwierdzenie",
            "Czy na pewno chcesz zamknąć aplikację?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            QApplication.quit()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close_application()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = TournamentManager()
    window.show()
    sys.exit(app.exec_())
