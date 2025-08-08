import random
import time
import csv
from datetime import datetime
import os
from pathlib import Path

# 模拟I2C设备地址
I2C_DEVICE_ADDR = 0x48


class I2CSensorSimulator:
    def __init__(self):
        self.i2c_addr = I2C_DEVICE_ADDR
        # 传感器数据范围
        self.temp_range = (20.0, 35.0)  # 温度: 20-35°C
        self.humidity_range = (30.0, 80.0)  # 湿度: 30-80%
        self.current_range = (0.5, 5.0)  # 电流: 0.5-5.0A
        self.voltage_range = (210.0, 240.0)  # 电压: 210-240V

        # 初始化报表存储
        self.report_dir = Path(__file__).resolve().parent.parent / "sensor_reports"
        os.makedirs(self.report_dir, exist_ok=True)
        self.report_path = self.report_dir / "sensor_data.csv"
        self._init_report_file()

    def _init_report_file(self):
        """初始化报表文件，添加status表头"""
        if not self.report_path.exists():
            with open(self.report_path, 'w', newline='') as f:
                writer = csv.writer(f)
                # 写表头，新增status列
                writer.writerow(["timestamp", "temperature", "humidity", "current", "voltage", "status"])

    # 修改save_to_report方法
    def save_to_report(self, data):
        """保存数据到报表"""
        with open(self.report_path, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                data["timestamp"],
                data["temperature"],
                data["humidity"],
                data["current"],
                data["voltage"],
                data["status"]  # 保存状态
            ])

    def _i2c_read(self, register):
        time.sleep(0.001)
        if register == 0x00:
            return round(random.uniform(*self.temp_range), 2)
        elif register == 0x01:
            return round(random.uniform(*self.humidity_range), 2)
        elif register == 0x02:
            return round(random.uniform(*self.current_range), 3)
        elif register == 0x03:
            return round(random.uniform(*self.voltage_range), 2)
        else:
            raise ValueError("Invalid I2C register address")

    def get_status(self, data):
        """计算状态：电流或电压大于中值则为fail"""
        current_mid = (self.current_range[0] + self.current_range[1]) / 2
        voltage_mid = (self.voltage_range[0] + self.voltage_range[1]) / 2
        return 'fail' if data['current'] > current_mid or data['voltage'] > voltage_mid else 'pass'

    def read_sensors(self):
        """读取所有传感器数据（不含status）"""
        return {
            "timestamp": datetime.now().isoformat(),
            "temperature": self._i2c_read(0x00),
            "humidity": self._i2c_read(0x01),
            "current": self._i2c_read(0x02),
            "voltage": self._i2c_read(0x03)
        }

    def save_to_report(self, data):
        """保存数据到报表，包含status"""
        with open(self.report_path, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                data["timestamp"],
                data["temperature"],
                data["humidity"],
                data["current"],
                data["voltage"],
                data["status"]  # 写入status
            ])

    def get_ranges_midpoint(self):
        """计算各传感器范围的中值"""
        return {
            'current': (self.current_range[0] + self.current_range[1]) / 2,
            'voltage': (self.voltage_range[0] + self.voltage_range[1]) / 2
        }

    def judge_status(self, data):
        """判断状态：电流或电压大于其中值则为fail，否则为pass"""
        midpoints = self.get_ranges_midpoint()
        if data['current'] > midpoints['current'] or data['voltage'] > midpoints['voltage']:
            return 'fail'
        return 'pass'

