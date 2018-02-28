# -*- coding: utf-8 -*-
# Author: Stefan Schöberl

import time
from picamera import PiCamera
from picamera.array import PiRGBArray
import car


def roadpos(arr):
    mid = len(arr) / 2
    left = mid
    right = mid
    while left >= 0 and arr[left] > 10:
        left -= 1
    while right < len(arr) and arr[right] > 10:
        right += 1
    return (left + right) / 2


resolution = (320, 180)

camera = PiCamera()
camera.resolution = resolution
camera.framerate = 32
camera.color_effects = (128, 128)
camera.contrast = 100
rawCapture = PiRGBArray(camera, size=resolution)

time.sleep(0.1)

print 'ready to drive'

car.forward()

try:
    lastFrame = time.time()
    prevAngle = 0
    for frame in camera.capture_continuous(rawCapture, format="rgb", use_video_port=True):
        image = frame.array

        # extract row
        row = image[int(len(image) - 40)]

        # average RGB-Values
        rowGrey = map(lambda a: (a[0] + a[1] + a[2]) / 3.0, row)

        road = roadpos(rowGrey) / float(len(rowGrey))

        delta = 0.1
        angle = min(max((road - 0.5) / delta, -1), 1)

        car.stear(angle)

        now = time.time()
        fps = 1 / (now - lastFrame)
        lastFrame = now
        print fps, 'FPS'

        rawCapture.truncate(0)

except KeyboardInterrupt:
    pass
finally:
    car.cleanup()
