import serial
import serial.tools.list_ports
import time

class ElectroBlocks:
    def __init__(self, baudrate=115200, timeout=2):
        self.ser = self._auto_connect(baudrate, timeout)
        self._wait_for_ready()

    def _auto_connect(self, baudrate, timeout):
        ports = list(serial.tools.list_ports.comports())
        for p in ports:
            if p.vid == 9025 and p.pid in (67, 16): # Arduino Uno or Mega
                try:
                    ser = serial.Serial(p.device, baudrate, timeout=timeout)
                    time.sleep(2)  # Give Arduino time to reset
                    return ser
                except serial.SerialException:
                    continue
        raise Exception("No Arduino Uno or Mega found.")

    def _wait_for_ready(self):
        self.ser.write(b"IAM_READY|")
        while True:
            if self.ser.in_waiting:
                line = self.ser.readline().decode().strip()
                if "System:READY" in line:
                    break

    def _send(self, cmd):
        self.ser.write((cmd + "|\n").encode())
        while True:
            if self.ser.in_waiting:
                line = self.ser.readline().decode().strip()
                if "DONE_NEXT_COMMAND" in line:
                    break

    def config_servo(self, pin):
        self._send(f"config:servo={pin}")

    def move_servo(self, pin, angle):
        self._send(f"s:{pin}:{angle}")

    def config_rgb(self, r_pin, g_pin, b_pin):
        self._send(f"config:rgb={r_pin},{g_pin},{b_pin}")

    def set_rgb(self, r, g, b):
        self._send(f"rgb:{r},{g},{b}")

    def config_lcd(self, rows=2, cols=16):
        self._send(f"config:lcd={rows},{cols}")

    def lcd_print(self, row, col, message):
        self._send(f"l:{row}:{col}:{message}")

    def lcd_clear(self):
        self._send("l:clear")

    def digital_write(self, pin, value):
        self._send(f"dw:{pin}:{value}")

    def close(self):
        if self.ser and self.ser.is_open:
            self.ser.close()