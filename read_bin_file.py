import csv
import struct
import sys
from   pathlib import Path

num_channels = 2
bytes_per_signal = 2
bytes_per_sample = 2 * num_channels * bytes_per_signal
def chunked_read( fobj, chunk_bytes = bytes_per_sample*1024 ):
    while True:
        data = fobj.read(chunk_bytes)
        if( not data ):
            break
        else:
            yield data

def bin2csv( binfile = None,  chunk_bytes = bytes_per_sample*1024 ):
    with open(binfile, 'rb') as b:
        count = 0
        for data in chunked_read(b, chunk_bytes = chunk_bytes):
            count += len(data)
            for i in range(0, len(data), 8):
                sig_i1, = struct.unpack('<h', data[i:i+2])
                sig_q1, = struct.unpack('<h', data[i+2:i+4])
                sig_i2, = struct.unpack('<h', data[i+4:i+6])
                sig_q2, = struct.unpack('<h', data[i+6:i+8])
                count +=1
                print(",".join([str(sig_i1), str(sig_q1), str(sig_i2), str(sig_q2)]))
    print( "Processed", str(count), "samples." )

bin2csv( "/tmp/rx_out.bin")