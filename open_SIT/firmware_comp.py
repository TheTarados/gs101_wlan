import re
import os
from fcntl import ioctl
import sys
from time import sleep
import pickle
import zlib

if len(sys.argv) != 2:
        print("Will transform the firmware in a form usable by cbd.py\n\
              Usage: python firmware_comp.py <file_path>")
        sys.exit(1)

file_path = sys.argv[1]

data = []

with open(sys.argv[1]) as f:
    for i in f.readlines():
        op = re.split('\(|,|\)| ', i)
        op = list(filter(None, op))
        match op[0]:
            case "write":
                wval = op[2].replace("\\x", "").replace("\"","").strip()
                wbuf = bytearray.fromhex(wval)
                data.append(wbuf)
                
data = pickle.dumps(data)
compressed_data = zlib.compress(data, level=9)


with open(sys.argv[1].split('.')[-2].split('/')[-1]+'.z', 'wb') as f:
    f.write(compressed_data)
