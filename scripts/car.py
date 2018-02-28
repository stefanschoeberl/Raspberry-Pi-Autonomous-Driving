# -*- coding: utf-8 -*-
# Author: Stefan Schöberl

import RPi.GPIO as GPIO


class DrivingState:
    BACKWARD = 2
    STOP = 0
    FORWARD = 1


ENGINE_IN1 = 3
ENGINE_IN2 = 2
ENGINE_EN1 = 4

SERVO = 21

state = DrivingState.STOP

LEFT_DC = 5.65
RIGHT_DC = 7.6
DELTA_DC = (RIGHT_DC - LEFT_DC) / 2
CENTER_DC = (RIGHT_DC + LEFT_DC) / 2

servoPWM = None


def setup():
    global state, servoPWM
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(ENGINE_IN1, GPIO.OUT)
    GPIO.setup(ENGINE_IN2, GPIO.OUT)
    GPIO.setup(ENGINE_EN1, GPIO.OUT)
    GPIO.setup(SERVO, GPIO.OUT)

    GPIO.output(ENGINE_EN1, GPIO.LOW)
    GPIO.output(ENGINE_IN1, GPIO.LOW)
    GPIO.output(ENGINE_IN2, GPIO.LOW)

    state = DrivingState.STOP

    servoPWM = GPIO.PWM(SERVO, 50)
    servoPWM.start(CENTER_DC)


def forward():
    global state
    GPIO.output(ENGINE_IN1, GPIO.HIGH)
    GPIO.output(ENGINE_IN2, GPIO.LOW)
    GPIO.output(ENGINE_EN1, GPIO.HIGH)
    state = DrivingState.FORWARD


def backward():
    global state
    GPIO.output(ENGINE_IN1, GPIO.LOW)
    GPIO.output(ENGINE_IN2, GPIO.HIGH)
    GPIO.output(ENGINE_EN1, GPIO.HIGH)
    state = DrivingState.BACKWARD


def stear(angle):
    servoPWM.ChangeDutyCycle(CENTER_DC + angle * DELTA_DC)


def stop():
    global state
    GPIO.output(ENGINE_EN1, GPIO.LOW)
    GPIO.output(ENGINE_IN1, GPIO.LOW)
    GPIO.output(ENGINE_IN2, GPIO.LOW)
    state = DrivingState.STOP


def cleanup():
    GPIO.cleanup()


setup()
