import pandas as pd
import matplotlib.dates as mdates
import datetime as dt

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class Dashboard(FigureCanvas):
    def __init__(self):
        self.fig = Figure()
        super().__init__(self.fig)

        self.ax = self.fig.add_subplot(111)
        self.ax.set_title("Sensor Dashboard")
        self.ax.set_xlabel("Time")

        (self.temp_line,) = self.ax.plot([], [], label="Temperature")
        (self.humidity_line,) = self.ax.plot([], [], label="Humidity")
        (self.sound_line,) = self.ax.plot([], [], label="Sound")
        (self.light_line,) = self.ax.plot([], [], label="Light")

        self.date_label = self.ax.text(
            1.0, 1.05,
            "",
            transform=self.ax.transAxes,
            ha="right", va="bottom",
            fontsize=10, color="gray"
        )

        self.ax.legend()

        self.reset()

    def reset(self):
        self.timestamps = []
        self.temp = []
        self.hum = []
        self.sound = []
        self.light = []

        self.temp_line.set_data([], [])
        self.humidity_line.set_data([], [])
        self.sound_line.set_data([], [])
        self.light_line.set_data([], [])

        self.date_label.set_text("No data")

        self.ax.relim()
        self.ax.autoscale_view()
        self.draw()


    def add_point(self, data):
        # data = dict with Time, Temperature, Humidity, Sound_Level, Light_Level
        time_str = data["Time"]
        try:
            ts = pd.to_datetime(time_str, format="%m/%d/%y %H:%M")
        except Exception:
            ts = pd.to_datetime(time_str, errors="coerce")
            if pd.isna(ts):
                print("Could not parse timestamp:", time_str)
                return

        self.timestamps.append(ts)
        self.temp.append(data["Temperature"])
        self.hum.append(data["Humidity"])
        self.sound.append(data["Sound_Level"])
        self.light.append(data["Light_Level"])

        self.temp_line.set_data(self.timestamps, self.temp)
        self.humidity_line.set_data(self.timestamps, self.hum)
        self.sound_line.set_data(self.timestamps, self.sound)
        self.light_line.set_data(self.timestamps, self.light)

        # update date label
        date = ts.strftime("%d-%m-%y")
        self.date_label.set_text(f"Date: {date}")

        # format x-axis as time
        self.ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
        self.fig.autofmt_xdate()

        self.ax.relim()
        self.ax.autoscale_view()
        self.draw()
