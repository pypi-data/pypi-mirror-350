import RPi.GPIO as GPIO
from .config import *
import time


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)     # Comment for debugging with the Warnings

# Set in ../config.py
VELUX_PIN_OPEN = GPIO_PIN_VOPEN
VELUX_PIN_STOP = GPIO_PIN_VSTOP 
VELUX_PIN_CLOSE = GPIO_PIN_VCLOSE

GPIO.setup(VELUX_PIN_OPEN, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(VELUX_PIN_STOP, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(VELUX_PIN_CLOSE, GPIO.OUT, initial=GPIO.HIGH)


def v_cleanup():
    GPIO.cleanup()

def pulse(pin):
    GPIO.output(pin, GPIO.LOW)
    time.sleep(0.2)
    v_cleanup()

def v_open():
    pulse(VELUX_PIN_OPEN)

def v_stop():
    pulse(VELUX_PIN_STOP)

def v_close():
    pulse(VELUX_PIN_CLOSE)

