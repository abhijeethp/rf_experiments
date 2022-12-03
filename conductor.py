import serial
import time
import subprocess as sp

num_cycles = 3
sampling_duration = num_cycles * 2
rx_config = {
    "frequency": 2000 * 10**6,
    "samplerate": 31 * 10**6,
    "bandwidth": 10 * 10**6,
    "gain": 40,
    "duration_s": 0.001
}

port = '/dev/ttyACM1'
baudrate = 9600

def num_samples(config):
    return config["samplerate"] * config["duration_s"]

def current_time():
    curtime_ms = time.time_ns() // 1_000_000
    s, ms = divmod(curtime_ms, 1000)
    return '%s.%03dZ' % (time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime(s)), ms)

def print_current_time(msg):
    print(current_time() + "," + msg)

def start(command):
    return sp.Popen(
        command,
        stdin=sp.PIPE,
        stdout=sp.PIPE,
        stderr=sp.PIPE,
        shell=True,
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
file_format = file_ext = "bin"
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

print_current_time(f"running_{num_cycles}_servo_cycles")
arduino.write(bytes(f'3 {num_cycles}', 'utf-8'))

t_end = time.time() + sampling_duration
with open('/tmp/ard_out.log', 'wb') as f:
    while time.time() < t_end:
        line = arduino.readline().decode('utf-8')
        if line == "" or line == "\n":
            continue
        curtime_ms = time.time_ns() // 1_000_000
        s, ms = divmod(curtime_ms, 1000)
        curtime = '%s.%03dZ' % (time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime(s)), ms)
        f.write(bytes(current_time() + "," + line, 'utf-8'))

print_current_time("waiting_for_bladerf_to_flush_buffers")
t_terminate =  time.time() + 15 # make sure bladerf flushes all buffers
while time.time() < t_terminate:
    continue

print_current_time("terminating_bladerf_cli")
terminate(p)




