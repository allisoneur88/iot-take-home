import pandas as pd
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QTextEdit, QVBoxLayout, QHBoxLayout

from mqtt_client import MqttHandler
from dashboard import Dashboard


class MainWindow(QMainWindow):
    def __init__(self, csv_file="Simulated_sensor_data.csv"):
        super().__init__()
        self.setWindowTitle("MQTT Python Demo")

        # data
        self.df = pd.read_csv(csv_file)
        self.index = 0

        # widgets
        self.send_button = QPushButton("Send Next Record")
        self.play_all_button = QPushButton("Play All")
        self.reset_button = QPushButton("Reset")
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.dashboard = Dashboard()

        # layout for buttons at the top
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.send_button)
        button_layout.addWidget(self.play_all_button)
        button_layout.addWidget(self.reset_button)

        # main layout
        layout = QVBoxLayout()
        layout.addLayout(button_layout)
        layout.addWidget(self.output, stretch = 1)
        layout.addWidget(self.dashboard, stretch = 5)

        # timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.send_next)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # mqtt 
        self.mqtt = MqttHandler()
        self.mqtt.received_callback = self.on_units_produced
        self.mqtt.sensor_callback = self.on_sensor_update
        self.mqtt.loop_start()

        # signals
        self.send_button.clicked.connect(self.send_next)
        self.play_all_button.clicked.connect(self.start_play)
        self.reset_button.clicked.connect(self.reset_index)

    def send_next(self):
        if self.index < len(self.df):
            row = self.df.iloc[self.index].to_dict()
            self.mqtt.publish_sensor_data(row)
            self.index += 1
        else:
            self.output.append("No more CSV records.")
            if self.timer.isActive():
                self.timer.stop()

    def start_play(self):
        self.index = 0
        self.timer.start(100)

    def reset_index(self):
        self.index = 0
        if self.timer.isActive():
            self.timer.stop()

        self.output.clear()
        self.dashboard.reset()

    def on_units_produced(self, message):
        self.output.append(f"[UnitsProduced] {message}")

    def on_sensor_update(self, data):
        self.dashboard.add_point(data)

    def closeEvent(self, event):
        self.mqtt.loop_stop()
        event.accept()
