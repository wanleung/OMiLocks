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
    PIN_UNLOCK = 20
    PIN_LOCK = 21
    PIN_STATE_CLOSE = 13
    PIN_OFF = 5
    PIN_DISABLE_LED = 6
    state = 0
    def __init__(self):
        state = 0
        system_state = 0

    def open(self):
        GPIO.setmode(GPIO.BCM)
        #GPIO.setwarnings(False)
        GPIO.setup(self.PIN_LOCK, GPIO.OUT)
        GPIO.setup(self.PIN_UNLOCK, GPIO.OUT)
        GPIO.setup(self.PIN_STATE_CLOSE, GPIO.IN)
        GPIO.setup(self.PIN_OFF, GPIO.IN)
        GPIO.setup(self.PIN_DISABLE_LED, GPIO.OUT)

    def close(self):
        GPIO.cleanup()

    def is_door_closed(self):
        return GPIO.input(self.PIN_STATE_CLOSE) == 0

    def is_system_off(self):
        return GPIO.input(self.PIN_OFF) == 0

    def unlock(self):
        GPIO.output(self.PIN_UNLOCK, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(self.PIN_UNLOCK, GPIO.LOW)

    def lock(self):
        GPIO.output(self.PIN_LOCK, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(self.PIN_LOCK, GPIO.LOW)

    def set_system_close(self, isClosed):
        if isClosed:
            GPIO.output(self.PIN_DISABLE_LED, GPIO.HIGH)
            self.system_state = 0 
        else:
            GPIO.output(self.PIN_DISABLE_LED, GPIO.LOW)
            self.system_state = 1


def loop(dc):
    ###
    # door deadbolt
    # O    C        6
    # O    O        4
    # C    C        1
    # C    O        5
    # Locking 3  Unlocking 2

    if dc.is_system_off() == False:
        if dc.system_state == 0:
            dc.set_system_close(False)

        if dc.state == 0:
            print dc.state
        elif dc.state == 1:
            print dc.state
        elif dc.state == 2:
            print dc.state
        elif dc.state == 3:
            print dc.state
        elif dc.state == 4:
            print dc.state
        elif dc.state == 5:
            print dc.state
        elif dc.state == 6:
            print dc.state
        else:
            print dc.state

    else:
        if dc.system_state == 1:
            dc.set_system_close(True)

    #if dc.is_door_closed():
    #    dc.unlock()
    #else:
    #    dc.lock()
    time.sleep(1)


if __name__ == '__main__':
    killer = GracefulKiller()
    doorchannel = HomeLock()
    doorchannel.open()
    if doorchannel.is_system_off():
        doorchannel.state = 0
        doorchannel.set_system_close(True)
    else:
        doorchannel.set_system_close(False)
        if doorchannel.is_door_closed():
            doorchannel.lock()
            doorchannel.state = 1
            time.sleep(1)
 
    while True:
        loop(doorchannel)
        if killer.kill_now:
            doorchannel.close()
            break

    print '==== Finished ===='
