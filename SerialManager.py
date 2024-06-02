import serial
import time
import threading
import re
from PacketList import PacketList

class SerialManager():

	timeout = 0.25

	def __init__(self, device, logging = False):
		self.device = device
		self.logging = logging
		self.start()

	def start(self):
		self.connect()
		self.reset()
		time.sleep(1)
		self.output = []
		self.packets = PacketList()
		self.processorThread = threading.Thread(target=self.process)
		self.run = True
		self.processorThread.start()

	def stop(self):
		self.run = False

	def reset(self):
		self.ser.setDTR(False)
		time.sleep(1)
		self.ser.flushInput()
		self.ser.setDTR(True)

	def connect(self, isolate=False):
		self.ser = serial.Serial()
		self.ser.port = self.device
		self.ser.timeout = self.timeout
		self.ser.baudrate = 115200
		self.ser.open()
		self.ser.read_all()

	def decToHex(self, dec):
		return '{:02x}'.format(int(dec))

	def sendPacket(self, packet, priority=0):
		_packet = packet.copy()
		_packet = [self.decToHex(x) for x in _packet]
		packetString = "".join(_packet)
		appended = self.safeAppend(packetString, priority)
		if not appended:
			return False, False, False

		packet.insert(0,0)
		timeinit = time.time()
		while (time.time() < timeinit+self.timeout):
			confirmationPacket = self.packets.search(packet)
			if not confirmationPacket == None:
				break
		if confirmationPacket == None:
			return True, False, False
		else:
			return True, True, int(confirmationPacket[len(confirmationPacket)-1]) == 1

	def safeAppend(self, packetString, priority):
		for item in self.output:
			if item[0] == packetString:
				return False
		self.output.append([packetString, priority])
		return True

	def awaitResponse(self, packet, timeout = None):
		if timeout == None:
			timeout = self.timeout
		timeinit = time.time()
		if self.logging:
			packetString = [str(x) for x in packet]
			with open("packets.log","a+") as file:
				file.write("awaiting "+"".join(packetString)+"\n")

		while (time.time() < timeinit+timeout):
			response = self.packets.search(packet)
			if not response == None:
				if self.logging:
					with open("packets.log","a+") as file:
						file.write("found "+"".join(packetString)+"\n")
				return response

		if self.logging:
			with open("packets.log","a+") as file:
				file.write("timeout "+" ".join(packetString)+"\n")

	def isPacket(self, string):
		matches = re.match("[0-9A-F]{1,48}", string)
		return matches != None

	def process(self):
		while self.run:
			self.output.sort(key=lambda x: x[1])
			if len(self.output) > 0:
				try:
					command = self.output.pop(0)
					if self.logging:
						packetString = [str(x) for x in command[0]]
						with open("packets.log","a+") as file:
							file.write("--> "+"".join(packetString)+"\n")
					self.ser.write((command[0]+"\n").encode())
				except:
					pass

			if self.ser.in_waiting:
				packet = self.ser.readline()
				packet = packet.decode().strip()
				isPacket = self.isPacket(packet)
				if isPacket:
					if self.logging:
						packetString = [str(x) for x in packet]
						with open("packets.log","a+") as file:
							file.write("<-- "+"".join(packetString)+"\n")
					chunks, chunk_size = len(packet), 2
					packet = [ packet[i:i+chunk_size] for i in range(0, chunks, chunk_size) ]
					packet = [ int(x, 16) for x in packet ]
					self.packets.append(packet)
				else:
					print (packet)



if __name__ == 	"__main__":
	s = SerialManager('/dev/arduino-r4', True)
	for i in range(0,10):
		init = time.time()
		accepted, received, recognized = s.sendPacket([1])
		end = time.time()
		#print (end - init, accepted, received, recognized);
	s.stop()
