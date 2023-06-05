import serial
import time

def led_on(status):
    ser = serial.Seial("com4", 9800, timeout=1)
    if status:
        ser.write("H")
        time.sleep(3)
        ser.write("L")
    pass