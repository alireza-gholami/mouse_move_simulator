import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import QTimer, Qt
import pyautogui

class MouseMoverApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.remaining_time = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.perform_action)
        self.stop_program = False
        self.distance = 0

    def initUI(self):
        self.setWindowTitle('Mausbewegung GUI')

        layout = QVBoxLayout()

        # Label und Eingabefeld für Distance
        self.distance_label = QLabel('Distance (Pixel):')
        layout.addWidget(self.distance_label)
        self.distance_input = QLineEdit()
        layout.addWidget(self.distance_input)

        # Label und Eingabefeld für Duration
        self.duration_label = QLabel('Duration (Sekunden):')
        layout.addWidget(self.duration_label)
        self.duration_input = QLineEdit()
        layout.addWidget(self.duration_input)

        # Anzeige der Restzeit
        self.time_display = QLabel('Restzeit: 0s')
        layout.addWidget(self.time_display)

        # Start-Button
        self.start_button = QPushButton('Starten')
        self.start_button.clicked.connect(self.start_moving)
        layout.addWidget(self.start_button)

        self.setLayout(layout)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.stop_program = True
            self.timer.stop()
            QMessageBox.information(self, "Abgebrochen", "Der Prozess wurde vorzeitig beendet.")
            event.accept()
        else:
            event.ignore()

    def perform_action(self):
        if self.remaining_time > 0 and not self.stop_program:
            self.time_display.setText(f'Restzeit: {self.remaining_time}s')
            self.remaining_time -= 1
            self.move_mouse_square(self.distance)
        else:
            self.timer.stop()
            if not self.stop_program:
                QMessageBox.information(self, "Fertig", "Der Prozess ist abgeschlossen.")
            self.stop_program = True

    def move_mouse_square(self, distance):
        if self.stop_program:
            return
        pyautogui.moveRel(distance, 0, duration=0.5)
        pyautogui.moveRel(0, distance, duration=0.5)
        pyautogui.moveRel(-distance, 0, duration=0.5)
        pyautogui.moveRel(0, -distance, duration=0.5)

    def start_moving(self):
        self.stop_program = False

        try:
            self.distance = int(self.distance_input.text())
            duration_move_time = int(self.duration_input.text())
        except ValueError:
            QMessageBox.critical(self, "Ungültige Eingabe", "Bitte gib gültige Zahlen ein.")
            return

        self.remaining_time = duration_move_time
        self.time_display.setText(f'Restzeit: {self.remaining_time}s')
        self.timer.start(1000)  # Timer alle 1 Sekunde auslösen

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MouseMoverApp()
    window.show()
    sys.exit(app.exec_())
