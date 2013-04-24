########## Thread Manager - thread_manager.py ##########

# Original Author: John Zeller

# The Thread Manager constantly checks the health of all threads, and if one dies, it calls
# for the exit of all other threads

import wx
import sys
import time
import threading

class ThreadManager(threading.Thread):
    def __init__(self, roverStatus):
        threading.Thread.__init__(self)
        self.roverStatus = roverStatus
        with self.roverStatus.roverStatusMutex:
            self.start_time = self.roverStatus.start_time

    def run(self):
        while 1:
            exit = 0
            # Check if Main Thread is alive every 1 second
            if (time.time() - self.start_time) > 1: # If more than 1 second has passed, check heartbeat
                self.start_time = time.time()   # Reset timer
                with self.roverStatus.roverStatusMutex:
                    mainThreadAlive = self.roverStatus.mainThreadAlive
                    if mainThreadAlive is False:    # Then mainThread died at least 1 second ago
                        exit = 1
                    elif mainThreadAlive == True:   # Then reset heartbeat to allow checking
                        self.roverStatus.mainThreadAlive = False
            # Check if all other threads are alive
            with self.roverStatus.roverStatusMutex:
                thread_list = self.roverStatus.thread_list
            for nThread in thread_list:
                if nThread.isAlive() is False:
                    exit = 1
            # If any threads have died, then exit all threads, including this one
            if exit == 1:
                with self.roverStatus.roverStatusMutex:
                    self.roverStatus.updaterThreadExit = True
                    self.roverStatus.receptionistThreadExit = True
                    self.roverStatus.drivejoyThreadExit = True
                    self.roverStatus.armjoyThreadExit = True
                    self.roverStatus.queuerThreadExit = True
                raise Exception("THREAD MANAGER: Another child thread has died. Terminating Thread Manager.")