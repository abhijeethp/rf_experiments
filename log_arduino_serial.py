import serial
import time
from datetime import datetime

port = '/dev/cu.usbmodem14401'
baudrate = 9600
arduino = serial.Serial(port=port, baudrate=baudrate, timeout=0.1)
time.sleep(10)
# curtime_ms = time.time_ns() // 1_000_000
# s, ms = divmod(curtime_ms, 1000)
# curtime = '%s.%03d' % (time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(s)), ms)
# print(curtime)

# arduino.write(bytes('1', 'utf-8')) # start the servo function
arduino.write(bytes('1', 'utf-8')) # start the servo function
time.sleep(10)
with open('output.log', 'wb') as f:
    while True:
        line = arduino.readline().decode('utf-8')
        # curtime_ms = time.time_ns() // 1_000_000
        # s, ms = divmod(curtime_ms, 1000)
        # curtime = '%s.%03d' % (time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(s)), ms)
        print(line)
        # f.write(bytes(str(curtime_ms) + " ( "+curtime+" ) " + " | " + line, 'utf-8'))