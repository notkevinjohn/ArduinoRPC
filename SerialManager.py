import serial
import time
import threading
from PacketList import PacketList

class SerialManager():

	timeout = 0.5

	def __init__(self, device, logging = False):
		self.device = device
		self.logging = logging
		self.connect()
		self.reset()
		time.sleep(1)
		self.packets = PacketList()
		self.listenerThread = threading.Thread(target=self.listen)
		self.listen = True
		self.listenerThread.start()

	def stop(self):
		self.listen = False

	def reset(self):
		self.ser.setDTR(False)
		time.sleep(1)
		self.ser.flushInput()
		self.ser.setDTR(True)

	def connect(self, isolate=False):
		self.ser = serial.Serial()
		self.ser.port = self.device
		self.ser.timeout = 0.1
		self.ser.baudrate = 9600
		self.ser.open()
		self.ser.read_all()

	def decToHex(self, dec):
		return '{:02x}'.format(int(dec)).upper()

	def sendPacket(self, packet):
		_packet = packet.copy()
		_packet = [self.decToHex(x) for x in _packet]
		packetString = "".join(_packet)
		self.ser.write((packetString+"\n").encode())
		if self.logging:
			ps = [str(x) for x in _packet]
			with open("packets.log","a+") as file:
				file.write("-->"+" ".join(ps)+"\n")
		packet.insert(0,0)
		timeinit = time.time()
		while (time.time() < timeinit+self.timeout):
			confirmationPacket = self.packets.search(packet)
			if not confirmationPacket == None:
				break
		if confirmationPacket == None:
			return False, False
		else:
			return True, int(confirmationPacket[len(confirmationPacket)-1]) == 1

	def awaitResponse(self, packet, timeout = None):
		if timeout == None:
			timeout = self.timeout
		timeinit = time.time()
		if self.logging:
			packetString = [str(x) for x in packet]
			with open("packets.log","a+") as file:
				file.write("awaiting "+" ".join(packetString)+"\n")

		while (time.time() < timeinit+timeout):
			response = self.packets.search(packet)
			if not response == None:
				if self.logging:
					with open("packets.log","a+") as file:
						file.write("found "+" ".join(packetString)+"\n")
				return response

		if self.logging:
			with open("packets.log","a+") as file:
				file.write("timeout "+" ".join(packetString)+"\n")


	def listen(self):
		while self.listen:
			packet = self.ser.readline()
			if len(packet) > 0:
				packet = packet.decode().strip()
				if self.logging:
					ps = [str(x) for x in packet]
					with open("packets.log","a+") as file:
						file.write("<--"+"".join(ps)+"\n")
				chunks, chunk_size = len(packet), 2
				packet = [ packet[i:i+chunk_size] for i in range(0, chunks, chunk_size) ]
				packet = [ int(x, 16) for x in packet ]
				self.packets.append(packet)




if __name__ == 	"__main__":
	s = SerialManager('/dev/arduino-mega', True)
	received, recognized = s.sendPacket([0])
	print (received, recognized)
	s.stop()
