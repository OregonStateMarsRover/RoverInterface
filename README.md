# Mars Rover Primary and Secondary Addresses (w/ Data)
* 1  - BeagleBone
     + 17 - RESERVED: Rover Alive Packet
* 2  - Left/Front Wheel     (speed, angle)
* 3  - Left/Middle Wheel    (speed, angle)
* 4  - Left/Rear Wheel      (speed, angle)
* 5  - Right/Front Wheel    (speed, angle)
* 6  - Right/Middle Wheel   (speed, angle)
* 7  - Right/Rear Wheel     (speed, angle)
* 8  - Arm                  (secondAddr, angle, angle_overflow)
     + 1 - Shoulder Motor
     + 2 - Elbow Motor
* 9  - Wrist
     + 1 - Angle Servo      (secondAddr, angle, angle_overflow)
     + 2 - Tilt Servo       (secondAddr, angle)
     + 3 - Scoop Actuate    (secondAddr, command)
     + 4 - Probe Actuate    (secondAddr, distance)
     + 5 - Probe Get Data   (secondAddr, request)
     + 6 - Get Voltage      (secondAddr, request)
* 10 - Tripod 
     + 1 - Horizontal Servo (secondAddr, angle)
     + 2 - Vertical Servo   (secondAddr, angle)
     + 3 - Zoom             (secondAddr, distance)
* 11 - MUX                  (camera_select)
* 12 - Package              (package_select)

# Mars Rover Packet Data Formats
* 1      - BeagleBone
            + 17 - RESERVED: Rover Alive Packet
* 2,3,4  - Left/Front,Middle,Rear Wheels
* 5,6,7  - Right/Front,Middle,Rear Wheels
* 8  - Arm
     + 1 - Shoulder Motor
     + 2 - Elbow Motor
* 9  - Wrist
     + 1 - Angle Servo
     + 2 - Tilt Servo
     + 3 - Scoop Actuate
     + 4 - Probe Actuate
     + 5 - Probe Get Data
     + 6 - Get Voltage
* 10 - Tripod
     + 1 - Horizontal Servo
     + 2 - Vertical Servo
     + 3 - Zoom
* 11 - MUX
* 12 - Package

# Mars Rover Code Flow

## GUI Class
* This is the start of the program.
* Starts RoverStatus()
* Starts all GUI modules
    + Pass self as parent to each
    + Pass roverStatus class to each
        - This is a pointer to this object
        - The roverStatus object will be updated and use by each module
* Starts JoyStick Module [TODO:]
    + Pass self as parent
        - Should refresh parent after updating roverStatus
    + Pass roverStatus class
        - JoyStick can update positions of axis and buttons
* Starts "listener"
    + Pass self as parent
        - Should refresh parent after update roverStatus
    + Pass roverStatus class
        - Update rover positions with data from rover

## RoverStatus Class
* drive_mode - selected drive mode
* wheel - array of 6 wheels
    + angle - `-90 to 90` angle of wheel
    + velo - velocity of wheel  
    + omega - turn rate of each wheel [TODO: not needed right now]
* angle - used for vector steering
* throttle - used for adjustment for max velocity of wheels
* arm_seg - Array of each arm piece
    + len - length of each arm
        - used for calculation
    + angle - angle relative to the other arm
        - used for calculation
        - used for moving arm to that position
* wrist_angle
* wrist_tilt
* scoop_open
* voltage 
* package_one
* package_two
* package_three
* package_four
* package_five
* package_six 
* soil_moisture
* conductivity
* salinity
* f_temp 
* c_temp 

## JoyStick Class
* Attributes
    + parent - GUI class
    + roverStatus - class that holds current data of rover
* Functions
    + OnEvent - any change in joystick controls update roverStatus
        - Change joystick attribute in roverStatus
        - refresh parent, so that parent knows that roverStatus has changed.

## Listener Class
* Attributs
    + parent - GUI class
    + roverStatus - class that holds current data of rover
* Functions
    + OnMessage - pase message and update roverStatus
        - Change wheel, arm, package, etc attributes in roverStatus
        - refresh parent, so that parent knows that roverStatus has changed.