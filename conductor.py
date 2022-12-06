import serial, sys
import time
import subprocess as sp

logfile = open('/tmp/exp_log_out.log', 'w')

# SAR CONFIG
num_cycles = 1
cycle_duration_s = 2 # guesstimate of how long a cycle takes to execute. Is okay for it to be longer but not shorter to prevent data loss
sampling_duration = num_cycles * cycle_duration_s

antenna_stand_still_duration_ms  = 25

rx_config = {
    "frequency": 2000 * 10**6,
    "samplerate": 31 * 10**6,
    "bandwidth": 10 * 10**6,
    "gain": 40,
    "duration_s": antenna_stand_still_duration_ms / 1000 / 4
}

port = '/dev/ttyACM0'
baudrate = 9600

# log to multiple outputs (file, sysout)! Use this instead of print for analysis + debugging
def log(msg):
    print(msg)
    logfile.write(msg)


def num_samples(config):
    return config["samplerate"] * config["duration_s"]

def current_time():
    curtime_ms = time.time_ns() // 1_000_000
    s, ms = divmod(curtime_ms, 1000)
    return '%s.%03dZ' % (time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime(s)), ms)

def log_current_time(msg):
    log(current_time() + "," + msg)

def start(command):
    return sp.Popen(
        command,
        stdin=sp.PIPE,
        stdout=sp.PIPE,
        stderr=sp.PIPE,
        shell=True,
    )

def write(process, message):
    # print(message)
    process.stdin.write(f"{message.strip()}\n".encode("utf-8"))
    process.stdin.flush()

def terminate(process):
    process.stdin.close()
    process.terminate()
    process.wait(timeout=0.2)


log_current_time("starting_bladerf_cli")
p = start("bladeRF-cli -i")
write(p, f"set agc off")
write(p, f"set frequency rx {rx_config['frequency']}")
write(p, f"set samplerate rx {rx_config['samplerate']}")
write(p, f"set bandwidth rx {rx_config['bandwidth']}")
write(p, f"set gain rx {rx_config['gain']}")
file_format = file_ext = "bin"
file_out_name = "/tmp/exp_rx_out"
rx_channels = ["1","2"]
rx_channels_str = ",".join(rx_channels)


log_current_time("connecting_arduino")
arduino = serial.Serial(port=port, baudrate=baudrate, timeout=0.1)
time.sleep(5)


log_current_time(f"running_{num_cycles}_servo_cycles")
arduino.write(bytes(f'3 {num_cycles}', 'utf-8'))


with open('/tmp/exp_ard_out.log', 'wb') as f:
    step_num = 0
    while True:
        line = arduino.readline().decode('utf-8').rstrip()
        if line == "" or line == "Status changed to 3":
            continue

        if line == "Status changed to 0":
            break
        
        log_current_time(f"starting_rx_for_step[{step_num}]_degree[{line}]")
        write(p,f"rx config file={file_out_name}_{step_num}.{file_ext} format={file_format} n={num_samples(rx_config) * len(rx_channels)} channel={rx_channels_str}; rx start;")
        f.write(bytes(current_time() + "," + line+"\n", 'utf-8'))
        step_num += 1


log_current_time("terminating_bladerf_cli")
terminate(p)

logfile.close()
