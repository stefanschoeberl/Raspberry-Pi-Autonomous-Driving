# -*- coding: utf-8 -*-
# Author: Stefan Schöberl

import time
import datetime
import struct
import numpy as np
from picamera import PiCamera
from picamera.array import PiRGBArray

resolution = (640, 480)

camera = PiCamera()
camera.resolution = resolution
camera.color_effects = (128, 128)
camera.contrast = 100
camera.iso = 800
data = PiRGBArray(camera)
time.sleep(1)

file_name = datetime.datetime.now().isoformat() + ".car"
camera.capture(data, format='rgb', use_video_port=True)
save_to = open(file_name, "w")
save_to.write(struct.pack('<d', 0.34))
np.save(save_to, data.array)
save_to.close()
