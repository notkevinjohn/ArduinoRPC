import time
from SerialManager import SerialManager

class NeoPixelController():
	def __init__(self, device):
		self.serialManager = SerialManager(device)

	def color(self, red, green, blue):
		self.serialManager.sendPacket([1, int(red), int(green), int(blue)])


	def chase(self, red, green, blue , delay, repeat):
		self.serialManager.sendPacket([2, red, green, blue, delay, repeat])

	def append(self, red, green, blue):
		self.serialManager.sendPacket([3, int(red), int(green), int(blue)])

if __name__ == "__main__":
	npc = NeoPixelController('/dev/arduino-r4')
	print ('Controller = npc')
