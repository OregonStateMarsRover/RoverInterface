1) In order to setup a serial connection over /dev/ttyUSB1, we must set 
	the correct ownership.
	a) If you were to type "ll /dev/ttyO0" into the BeagleBone 
		terminal, you would see something like:
		crw------- 1 ubuntu tty 251, 0 Nov  2 22:39 /dev/ttyO0
	b) If you were to type "ll /dev/ttyUSB1" into the laptop terminal,
		you should see something like:
		crw-rw----   1 root  dialout 188,   0 Nov  8 16:21 ttyUSB1
	c) To change this type:
		sudo chown rover:rover /dev/ttyUSB1
	d) Now when you type "ll /dev/ttyUSB1" into the laptop terminal,
		you should see something like:
		crw-rw----   1 rover rover   188,   1 Nov  8 16:24 ttyUSB1
2) Install wxPython 2.8
	a) First make sure that you have Python installed
	b) Install wxGTK 2.8 with the command, 'sudo apt-get install python-wxgtk2.8'
	c) Run the command, 'apt-get source -d wxwidgets2.8'
	d) Now run, 'dpkg-source -x wxwidgets2.8_2.8.12.1-6ubuntu2.dsc'
	e) cd wxwidgets2.8-2.8.12.1
	f) cd wxPython
	g) Now run the command, 'sudo python setup.py install'
	h) wxPython and wxWidgets are now successfully installed!
