import serial
import time

class CRSFDriver:
    """Low-level driver for CRSF (HappyModel ES24TX)"""
    def __init__(self, port, baudrate=420000):
        self.port = port
        try:
            self.ser = serial.Serial(port, baudrate, timeout=0.1)
            print(f"[+] CRSF Driver initialized on {port}")
        except Exception as e:
            print(f"[!] Failed to open {port}: {e}")
            self.ser = None

    def _crc8(self, payload):
        """CRC8 for CRSF"""
        crc = 0
        for byte in payload:
            crc ^= byte
            for _ in range(8):
                if crc & 0x80:
                    crc = (crc << 1) ^ 0xD5
                else:
                    crc <<= 1
        return crc & 0xFF

    def pack_channels(self, channels):
        """
        Assemble 16 channels (every is 11 bits) n 22 bytes of the payload
        Channel inverval values: 172-1811 (eq. to 1000-2000 us).
        """
        payload = bytearray(22)
        # TEMPORARY CAP
        # IN REAL WORK - PACKAFING OF 11-bit values
        return payload

    def send_rc(self, roll=1500, pitch=1500, throttle=1000, yaw=1500):
        if not self.ser: return

        # AETR Mapping (Roll, Pitch, Throttle, Yaw) + Aux channels
        channels = [roll, pitch, throttle, yaw] + [1000]*12
        payload = self.pack_channels(channels)

        # CRSF Structure: [Sync, Length, Type, Payload, CRC]
        # Sync = 0xC8, Type = 0x16 (RC Channels)
        packet = bytearray([0xC8, 24, 0x16]) + payload
        packet.append(self._crc8(packet[2:]))
        
        self.ser.write(packet)
        print(f"[CRSF TX] R:{roll:.0f} P:{pitch:.0f} T:{throttle} Y:{yaw:.0f}")
