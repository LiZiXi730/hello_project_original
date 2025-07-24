import threading
import time
from .sensor_simulator import I2CSensorSimulator

class SensorDataCollector:
    def __init__(self, interval=5):
        self.interval = interval  # 数据采集间隔(秒)
        self.running = False
        self.thread = None
        self.sensor = I2CSensorSimulator()

    def start(self):
        """启动数据采集线程"""
        self.running = True
        self.thread = threading.Thread(target=self._collect_loop)
        self.thread.daemon = True
        self.thread.start()

    def stop(self):
        """停止数据采集"""
        self.running = False
        if self.thread:
            self.thread.join()

    def _collect_loop(self):
        """循环采集数据"""
        while self.running:
            data = self.sensor.read_sensors()
            self.sensor.save_to_report(data)
            time.sleep(self.interval)

# 初始化数据收集器(每5秒采集一次)
data_collector = SensorDataCollector(interval=5)