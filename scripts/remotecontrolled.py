# -*- coding: utf-8 -*-
# Author: Stefan Schöberl

import socket
import struct
import car

try:
    port = 5555
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(("", port))

    print "waiting on port:", port

    data = bytearray(10)

    while True:
        s.recvfrom_into(data)

        direction = data[0]
        angle = struct.unpack_from('<d', data, 1)[0]

        if direction == 0:
            car.stop()
        elif direction == 1:
            car.forward()
        elif direction == 2:
            car.backward()

        car.stear(angle)
except KeyboardInterrupt:
    pass
except:
    raise
finally:
    car.cleanup()
