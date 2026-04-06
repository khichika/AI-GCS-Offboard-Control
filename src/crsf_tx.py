import serial
import time

class CRSFDriver:
    def __init__(self, port, baudrate=420000):
        self.port = port
        self.ser = serial.Serial(port, baudrate, timeout=0.01) # Маленький таймаут для чтения
        self.vbat = 0.0

    def receive_telemetry(self):
        """Читает входящие данные от ELRS модуля"""
        if self.ser.in_waiting > 0:
            data = self.ser.read(self.ser.in_waiting)
            # Ищем пакет телеметрии (Type 0x08 - Battery/GPS)
            # В CRSF пакетах вольтаж обычно передается в определенном смещении
            for i in range(len(data) - 5):
                if data[i] == 0xC8 and data[i+2] == 0x08: # Sync + Battery Type
                    # Упрощенный пример парсинга: вольтаж в 10-х долях вольта
                    raw_v = (data[i+3] << 8) | data[i+4]
                    self.vbat = raw_v / 10.0
                    print(f"[TELEMETRY] Battery Voltage: {self.vbat}V")

    def send_rc(self, roll=1500, pitch=1500, throttle=1000, yaw=1500):
        # ... (код упаковки пакета остается прежним) ...
        # packet = self.pack_channels(channels)
        # self.ser.write(packet)
        
        # Сразу после отправки проверяем, не пришло ли чего в ответ
        self.receive_telemetry()
