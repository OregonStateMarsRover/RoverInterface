#Initial draft: Mike Fortner
#this class is meant to represent the rover arm and give methods for controlling the arm and querying its state

#note that this class so far has been written without testing and that I'm making some assumptions about how the arm angles will be measured and represented.
#I am meaasuring the angles in degrees 
#The shoulder angle is measured from verticle with zero being straight up
#The elbow angle is the relative angle between the two arm segments, measured counter-clockwise from the segment attached to the soulder
#The wrist angle is the relative angle between the forearm and the hand, measured clockwise from the forearm

#under this system, the angles should stay between 0 and 180 degrees, if my understanding of the arm is correct
#the final orientation of the wrist (measured from vertical like the shoulder) is shoulder_angle - elbow_angle + wrist_angle

class RoverArm(object):
	#these three represent the current measured position of the joints.  The arbitrary default looks somethinglike this: /\_  
	shoulder_angle = 30	
	elbow_angle = 60  
	wrist_angle = 120

	y_const = 5 #tuning constant for movement speed, totally guessed and should be tested/tuned
	z_const = 5

	shoulder_limits = (0,180)
	elbow_limits = (0,180)
	wrist_limits = (0,180)

	def calculate_motion(self, desired_y, desired_z):
	"""Takes inputs from the controller and calculates new joint angles based on the current positions
	desired_y: real number between 1 (fast up) and -1 (fast down) 
	desired_z: real number between 1 (fast forward) and -1(fast back)
	retval: returns a tuple of joint angles to be given to the firmware as set points

	The y direction is controlled entirely by rotating the shoulder, for simplicity
	The z direction is controlled by flexing the elbow and having the shoulder/wrist move equal amounts to maintain the orientation of the wrist"""
		new_shoulder = self.shoulder_angle + desired_y*y_const + desired_z*z_const*(1)  
		new_elbow = self.elbow_angle + desired_z*z_const*(2)
		new_wrist = self.wrist_angle + desired_z*z_const*(1)

		#enforce limits on movement
		#if the controller tells the arm to move somewhere it can't, the arm will simply ignore that part of the command
		#it's up to the pilot to notice
		if new_shoulder < shoulder_limits[0]:
			new_shoulder = shoulder_limits[0]
		if new_shoulder > shoulder_limits[1]:
			new_shoulder = shoulder_limits[1]

		if new_elbow < elbow_limits[0]:
			new_elbow = elbow_limits[0]
		if new_elbow > elbow_limits[1]:
			new_elbow = elbow_limits[1]

		if new_wrist < wrist_limits[0]:
			new_wrist = wrist_limits[0]
		if new_wrist > wrist_limits[1]:
			new_wrist = wrist_limits[1]

		return (new_shoulder, new_elbow, new_wrist)


	def get_position(self):
		return (self.shoulder_angle, self.elbow_angle, self.wrist_angle)