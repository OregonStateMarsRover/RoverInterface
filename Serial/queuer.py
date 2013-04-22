########## Queuer - queuer.py ##########

# Original Author: John Zeller

# The Queuer looks at Rover_Status to determine, based on the values of the
# Joy, what address, speed and angle commands are necessary. It then adds
# these commands in the form of a tuple (addr, speed, angle) to the receptionist_queue

import time
import threading
from roverpacket import *
from bus import *
from joy import *


class Queuer(threading.Thread):
    def __init__(self, gui, receptionist_queue, roverStatus):
        threading.Thread.__init__(self)
        self.gui = gui
        self.receptionist_queue = receptionist_queue
        self.roverStatus = roverStatus
        self.waitTime = 0.1  # Wait 20ms between packet cycles

    def run(self):
        while 1:
            # Make Joy Drive Commands
            #print "queue size: ",self.receptionist_queue.qsize()
            # WARNING: If there is ever an issue with crashing, double check that UpdateMath isn't being called from some other thread.
            self.gui.UpdateMath()
            drive_commands = self.poll_drive_command()
            drive_commands = self.assemble_drive_packet(drive_commands)
            with self.roverStatus.queueMutex:
                for command in drive_commands:
                    self.receptionist_queue.put(command)
            # Make Joy Arm Commands
                # Do something
            # Make Button Commands
            # self.receptionist_queue.put(self.poll_button_command())
            #print "Packet " + str(count) + "\n" + \
            #    str(int(round(self.roverStatus.wheel[0]['velo'] * 98))) + "\t" +\
            #    str(int(round(self.roverStatus.wheel[1]['velo'] * 98))) + "\t" +\
            #    str(int(round(self.roverStatus.wheel[2]['velo'] * 98))) + "\t" +\
            #    str(int(round(self.roverStatus.wheel[3]['velo'] * 98))) + "\t" +\
            #    str(int(round(self.roverStatus.wheel[4]['velo'] * 98))) + "\t" +\
            #    str(int(round(self.roverStatus.wheel[5]['velo'] * 98)))
            # print "Wheel 1: " + str(self.roverStatus.wheel[0]['velo'])
            # print "Wheel 2: " + str(self.roverStatus.wheel[1]['velo'])
            # print "Wheel 3: " + str(self.roverStatus.wheel[2]['velo'])
            # print "Wheel 4: " + str(self.roverStatus.wheel[3]['velo'])
            # print "Wheel 5: " + str(self.roverStatus.wheel[4]['velo'])
            # print "Wheel 6: " + str(self.roverStatus.wheel[5]['velo'])
            # print " "
            #print " "
            time.sleep(self.waitTime)

    def assemble_drive_packet(self, drive_commands):
        packet_list = []
        for command in drive_commands:
                wheelAddr, velocity, angle = command
                packet = BogiePacket(wheelAddr, velocity, angle)
                packet = packet.msg()  # Serializes packet
                packet_list.append(packet)
        return packet_list

    def poll_drive_command(self):
        # Returns list of 6 tuples of drive commands in the form
        # (wheelAddr, velocity, angle)
        command_list = []
        for wheelAddr in range(2, 8):
            with self.roverStatus.roverStatusMutex:
                velocity = self.roverStatus.wheel[wheelAddr - 2]['velo']
            if wheelAddr <= 4:
                velocity = round(velocity * 98)
            if wheelAddr > 4:
                velocity = -(round(velocity * 98))
            velocity = self.intToByte(velocity)
            with self.roverStatus.roverStatusMutex:
                angle = self.roverStatus.wheel[wheelAddr - 2]['angle']
            angle = round(self.intToByte(angle))
            cmd = wheelAddr, velocity, angle
            command_list.append(cmd)

        # Emergency Stop All Systems - Middle Button
        with self.roverStatus.joyMutex:
            if self.roverStatus.drive_joy_states['Middle'] == 1:
                command_list = []   # Overwrite old command list
                for wheelAddr in range(2, 8):
                    cmd = wheelAddr, 0, 0
                    command_list.append(cmd)

        return command_list

    def poll_arm_command(self):
        # Returns list of 3 tuples of arm commands in the form
        # (addr, speed, angle)
        nothing = 0

    def poll_button_command(self):
        # Returns 1 tuple for a button command in the form (addr, data)
        #
        command = None
        # Tripod Controls - (addr, vert_angle, horz_angle) - Angles -100 to 100
        # Angles should be persistent, meaning that this should change the
        # tripod angle state in roverStatus, and then that status should be
        # used to update the tripod command, if it needs updating

        return command

    def intToByte(self, int_var):
        # Description: Takes in an integer representation (-127 to 127) of
        #              speed and returns the byte representation that the
        #              bogie controllers use.
        #              (Reverse: 0-127) (Positive: 255-128)
        # NOTE: Does not work for RT or LT

        byte_var = 0
        if (int_var <= 0) and (int_var >= -127):
            byte_var = abs(int_var)  # Converts 0 to -127 -> 0 to 127
        elif (int_var >= 0) and (int_var <= 127):
            byte_var = -(int_var) + 255  # Converts 0 to 127 -> 255 to 128

        return byte_var

    def byteToInt(self, byte_var):
        # Description: Takes in a byte representation (Reverse: 0-127)
        #              (Positive: 255-128) of speed and returns the integer
        #              representation (-127 to 127)

        int_var = 0
        if (byte_var >= 0) and (byte_var <= 127):
            int_var = -(byte_var)  # Converts 0 to 127 -> 0 to -127
        elif (byte_var <= 255) and (byte_var >= 128):
            int_var = abs(byte_var - 255)  # Converts 255 to 128 -> 0 to 127

        return int_var
