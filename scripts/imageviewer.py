# -*- coding: utf-8 -*-
# Author: Stefan Schöberl

import numpy as np
import matplotlib.pyplot as plt
import struct
import sys
import os.path

# check if path given
if len(sys.argv) < 2:
    exit()

file_name = sys.argv[1]

plt.ion()
plt.show()

for i in range(1, len(sys.argv)):
    file_name = sys.argv[i]
    if os.path.isfile(file_name):
        load_from = file(file_name, "r")
        angle = struct.unpack('<d', load_from.read(8))[0]
        data = np.load(load_from)
        load_from.close()
        plt.imshow(data, interpolation='nearest')
        plt.title("{}\n{} - {}".format(os.path.basename(file_name), data.shape, angle))
    raw_input("")
