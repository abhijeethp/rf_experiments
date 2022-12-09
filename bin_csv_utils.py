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

def bin2csv_row(data, num_channels = 2):
    sig_i1, = struct.unpack('<h', data[0:2])
    sig_q1, = struct.unpack('<h', data[2:4])
    
    if num_channels == 1:
        return sig_i1, sig_q1

    sig_i2, = struct.unpack('<h', data[4:6])
    sig_q2, = struct.unpack('<h', data[6:8])
    return sig_i1, sig_q1, sig_i2, sig_q2

def bin2csv( binfile = None,  chunk_bytes = bytes_per_sample*1024 ):
    output = []
    with open(binfile, 'rb') as b:
        for data in chunked_read(b, chunk_bytes = chunk_bytes):
            for i in range(0, len(data), 8):
                sig_i1, sig_q1, sig_i2, sig_q2 = bin2csv_row(data[i:i+8])
                output.append([sig_i1, sig_q1, sig_i2, sig_q2])
    return output