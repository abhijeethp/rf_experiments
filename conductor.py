import serial
import time
import subprocess as sp

rx_config = {
    "frequency": 2000 * 10**6,
    "samplerate": 60 * 10**6,
    "bandwidth": 10 * 10**6,
    "gain": 40,
    "duration_s": 0.1
}

port = '/dev/ttyACM0'
baudrate = 9600

def num_samples(config):
    return config["samplerate"] * config["duration_s"]

def current_time():
    curtime_ms = time.time_ns() // 1_000_000
    s, ms = divmod(curtime_ms, 1000)
    return '%s.%03d' % (time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(s)), ms)

def print_current_time(msg):
    print(current_time() + " | " + msg)

def start(command):
    return sp.Popen(
        command,
        stdin=sp.PIPE,
        stdout=sp.PIPE,
        stderr=sp.PIPE,
        shell=True
    )

def read(process):
    return process.stdout.readline().decode("utf-8").strip()

def write(process, message):
    process.stdin.write(f"{message.strip()}\n".encode("utf-8"))
    process.stdin.flush()

def terminate(process):
    process.stdin.close()
    process.terminate()
    process.wait(timeout=0.2)


print_current_time("starting_bladerf_cli")
p = start("bladeRF-cli -i")
write(p, f"set agc off")
write(p, f"set frequency rx {rx_config['frequency']}")
write(p, f"set samplerate rx {rx_config['samplerate']}")
write(p, f"set bandwidth rx {rx_config['bandwidth']}")
write(p, f"set gain rx {rx_config['gain']}")
file_format = file_ext = "csv"
file_out_name = "/tmp/rx_out"
rx_channels = ["1","2"]
rx_channels_str = ",".join(rx_channels)
write(p,f"rx config file={file_out_name}.{file_ext} format={file_format} n={num_samples(rx_config) * len(rx_channels)} channel={rx_channels_str}")


print_current_time("connecting_arduino")
arduino = serial.Serial(port=port, baudrate=baudrate, timeout=0.1)
time.sleep(5)

print_current_time("starting_rx")
write(p, "rx start")
write(p, "rx wait")

print_current_time("starting_servo")
arduino.write(bytes('1', 'utf-8'))

t_end = time.time() + 15
with open('/tmp/ard_out.log', 'wb') as f:
    while time.time() < t_end:
        line = arduino.readline().decode('utf-8')
        curtime_ms = time.time_ns() // 1_000_000
        s, ms = divmod(curtime_ms, 1000)
        curtime = '%s.%03d' % (time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(s)), ms)
        f.write(bytes(current_time() + " | " + line, 'utf-8'))

print_current_time("terminating_bladerf_cli")
terminate(p)
print_current_time("stopping_servo")
arduino.write(bytes('0', 'utf-8'))




