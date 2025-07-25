# hello_app/tasks.py
import threading
import time
from .sensor_simulator import I2CSensorSimulator

class SensorDataCollector:
    def __init__(self, interval=5):
        self.interval = interval
        self.running = False
        self.thread = None
        self.sensor = I2CSensorSimulator()

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._collect_loop)
        self.thread.daemon = True
        self.thread.start()

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()

    def _collect_loop(self):
        while self.running:
            data = self.sensor.read_sensors()
            # 计算并添加status
            data['status'] = self.sensor.get_status(data)
            self.sensor.save_to_report(data)
            time.sleep(self.interval)

data_collector = SensorDataCollector(interval=5)