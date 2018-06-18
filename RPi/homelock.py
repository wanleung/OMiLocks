#!/usr/bin/python

import RPi.GPIO as GPIO
import time
import signal

class GracefulKiller:
    kill_now = False
    def __init__(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, signum, frame):
        self.kill_now = True

class HomeLock:
    ### Add param
    PIN_UNLOCK = 21
    PIN_LOCK = 20
    PIN_STATE_CLOSE = 13
    state = 0
    def __init__(self):
        state = 0

    def open(self):
        GPIO.setmode(GPIO.BCM)
        #GPIO.setwarnings(False)
        GPIO.setup(self.PIN_LOCK, GPIO.OUT)
        GPIO.setup(self.PIN_UNLOCK, GPIO.OUT)
        GPIO.setup(self.PIN_STATE_CLOSE, GPIO.IN)

    def close(self):
        GPIO.cleanup()

    def is_door_closed(self):
        return GPIO.input(self.PIN_STATE_CLOSE) == 1

    def unlock(self):
        GPIO.output(self.PIN_UNLOCK, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(self.PIN_UNLOCK, GPIO.LOW)

    def lock(self):
        GPIO.output(self.PIN_LOCK, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(self.PIN_LOCK, GPIO.LOW)
 


def loop(dc):
    print dc.is_door_closed()
    if dc.is_door_closed():
        dc.unlock()
    else:
        dc.lock()
    time.sleep(1)


if __name__ == '__main__':
    killer = GracefulKiller()
    doorchannel = HomeLock()
    doorchannel.open()
    while True:
        loop(doorchannel)
        if killer.kill_now:
            doorchannel.close()
            break

    print '==== Finished ===='
