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
