import sys
import serial

def exit_msg():
	print "Usage: {0} <ID> <Instruction> <P1> <P2> ... <PN>".format(sys.argv[0].split("\\")[-1])
	sys.exit(0)

def parse_input():
	args = sys.argv
	if len(args) < 3:
		exit_msg()
	try:
		ID = int("0" + args[1], 16)
		Instruction = int("0" + args[2], 16)
	except:
		exit_msg()

	x = 3
	parameters = []
	while 1:
		try:
			parameters.append(int("0" + args[x], 16))
		except:
			break
		x += 1

	return (ID, Instruction, parameters)

if __name__ == '__main__':
	ID, Instruction, parameters = parse_input()

	Length = len(parameters) + 2

	packet = bytearray([0xFF, 0xFF, ID, Length, Instruction])
	for x in range(Length - 2):
		if len(parameters) != 0:
			packet.append(parameters[x])

	Checksum = ID + Length + Instruction
	for x in range(Length - 2):
		Checksum += parameters[x]
	Checksum = ~(Checksum)
	PreChecksum = Checksum
	Checksum = int("0" + hex(Checksum)[-2:], 16)
	packet.append(Checksum)

	print "Packet: " + repr(packet)

	print "ID:", hex(ID)
	print "Instruction:", hex(Instruction)
	print "Length (as Int):", Length
	for x in range(Length - 2):
		print "Parameter", x + 1, ":", hex(parameters[x])
	print "Checksum (before cutting):", hex(PreChecksum)
	print "Checksum (after cutting):", hex(Checksum)

        try:
		bus = serial.Serial(port="/dev/ttyUSB0", 
	                                baudrate="1000000")
	        bus.write(packet)
	except AttributeError as e:
		print e
