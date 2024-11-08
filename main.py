import sys
import time
import pyautogui
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox

class MouseMoverApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

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

        # Start-Button
        self.start_button = QPushButton('Starten')
        self.start_button.clicked.connect(self.start_moving)
        layout.addWidget(self.start_button)

        self.setLayout(layout)

    def move_mouse_square(self, distance):
        pyautogui.moveRel(distance, 0, duration=0.5)
        time.sleep(0.5)
        pyautogui.moveRel(0, distance, duration=0.5)
        time.sleep(0.5)
        pyautogui.moveRel(-distance, 0, duration=0.5)
        time.sleep(0.5)
        pyautogui.moveRel(0, -distance, duration=0.5)
        time.sleep(0.5)

    def start_moving(self):
        try:
            distance = int(self.distance_input.text())
            duration_move_time = int(self.duration_input.text())
        except ValueError:
            QMessageBox.critical(self, "Ungültige Eingabe", "Bitte gib gültige Zahlen ein.")
            return

        QMessageBox.information(self, "Start", "Der Mausbewegungsprozess beginnt in 3 Sekunden.")
        time.sleep(3)

        start_time = time.time()
        while (time.time() - start_time) <= duration_move_time:
            self.move_mouse_square(distance)

        QMessageBox.information(self, "Fertig", "Der Prozess ist abgeschlossen.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MouseMoverApp()
    window.show()
    sys.exit(app.exec_())
