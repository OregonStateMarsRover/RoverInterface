#	roverpacket.py
#	Author: Mike Fortner
#	This file defines the packet protocol used on the 2013 mars rover.
#	new RoverPackets can be made directly from strings or lists of byte values, or they can be read from a serial port with RoverPacket.from_rx(port)
#
#
#


class RoverPacket(object):
    start_byte = 0xCA
    escape_byte = 0x5C
    null_byte = 0x00
    max_byte = 0xFF
    escaped_bytes = {start_byte: 2, escape_byte: 3, null_byte: 4, max_byte: 5}
    unescaped_bytes = dict((a, b) for b, a in escaped_bytes.iteritems())

    def __init__(self, addr, content):
        self.addr = addr
        self.content = bytearray(content)
        self.compute_full_message()

    def compute_full_message(self):
        escaped_content = self.escape_content(self.content)
        self.length = len(escaped_content) + 1  # length of escaped content plus checksum
        self.message = bytearray([self.start_byte, self.addr, self.length]) + escaped_content
        self.checksum = (
            (~sum(self.message)) & 0xFF)  # bitwise complement of the sum of the other bytes, clipped to a single byte
        self.full_message = self.message + bytearray([self.checksum])

    def escape_content(self, content):
        escaped_content = bytearray()
        for byte in content:
            if byte in self.escaped_bytes.keys():
                escaped_content.append(self.escape_byte)
                escaped_content.append(self.escaped_bytes[byte])
            else:
                escaped_content.append(byte)
        return escaped_content

    def unescape_content(self, escaped_content):
        next_byte_escaped = False
        content = bytearray()
        for byte in escaped_content:
            if next_byte_escaped:
                content.append(self.unescaped_bytes[byte])
                next_byte_escaped = False
            elif byte == self.escape_byte:
                next_byte_escaped = True
            elif byte in self.escaped_bytes.keys():
                raise Exception("Error: unexpected control character was seen without preceding escape character")
            else:
                content.append(byte)
        return content

    def append(self, bytes):
        self.content.append(bytes)
        self.compute_full_message()

    def tx(self, port):
        port.write(self.full_message)

    def rx(self, port):
        """receive a rover protocol packet on "port." There should be bytes already waiting on the port when this function is called"""
        if (not port.inWaiting()):
            raise Exception("Error: no bytes waiting on port")
        start = int(port.read().encode("hex"), 16)

        if start != self.start_byte:
            raise Exception("start byte error %s != %s" % (start, self.start_byte))
        self.addr = int(port.read().encode("hex"), 16)
        length = int(port.read().encode("hex"), 16)
        escaped_content = bytearray(port.read(length - 1))

        self.content = self.unescape_content(escaped_content)
        self.compute_full_message()

        checksum = int(port.read().encode("hex"), 16)
        if checksum != self.checksum:
            raise Exception("checksum error %s != %s" % (checksum, self.checksum))

    @classmethod
    def from_rx(cls, port):
        new = cls(0, [])
        new.rx(port)
        return new

    def msg(self):
        return self.full_message

    def __str__(self):
        return str(list(self.full_message))

    def __repr__(self):
        return repr(self.full_message)

    def __len__(self):
        return len(self.full_message)

    def __hex__(self):
        return "0x" + "".join(["%.2x" % i for i in self.full_message])

    def __add__(self, other):
        if type(other) != type(self):
            raise TypeError
        return RoverPacket(self.addr, self.content + other.content)


class BogiePacket(RoverPacket):
    def __init__(self, addr, speed, turning):
        content = [int(speed), int(turning)]
        # print content
        RoverPacket.__init__(self, addr, content)

    @classmethod
    def from_rx(cls, port):
        new = cls(0, 0, 0)
        new.rx(port)
        if (len(new.content) != 2):
            raise Exception("Bogie packet contents had unexpected length of %d" % len(new))
        return new
