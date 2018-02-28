# -*- coding: utf-8 -*-
# Author: Stefan Schöberl

import datetime
import socket
import struct
import threading
import time

import numpy as np
from picamera import PiCamera
from picamera.array import PiRGBArray

import car

current_angle = -10
resolution = (200, 150)
request_end = False


class CaptureThread (threading.Thread):
    def run(self):
        camera = PiCamera()
        camera.resolution = resolution
        camera.contrast = 100
        camera.color_effects = (127, 127)
        time.sleep(1)
        print "recording"
        raw = PiRGBArray(camera)

        for frame in camera.capture_continuous(raw, format='rgb', use_video_port=True):
            file_name = datetime.datetime.now().isoformat() + ".car"
            save_to = open(file_name, "w")
            save_to.write(struct.pack('<d', current_angle))
            np.save(save_to, frame.array)
            save_to.close()

            raw.truncate(0)

            if request_end:
                print "end recording"
                break


capture_thread = CaptureThread()

try:
    port = 5555
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(("", port))

    print "waiting on port:", port

    data = bytearray(10)

    # wait for first packet
    s.recv_into(data)
    capture_thread.start()

    while True:
        s.recvfrom_into(data)

        direction = data[0]
        current_angle = struct.unpack_from('<d', data, 1)[0]

        if direction == 0:
            car.stop()
        elif direction == 1:
            car.forward()
        elif direction == 2:
            car.backward()

        car.stear(current_angle)
except KeyboardInterrupt:
    pass
except:
    raise
finally:
    request_end = True
    capture_thread.join()
    car.cleanup()
