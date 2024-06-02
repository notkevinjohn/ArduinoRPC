class PacketList():

	limit = 100

	def __init__(self):
		self.packets = []

	def append(self, packet):
		self.packets.append(packet)
		if len(self.packets) > self.limit:
			self.packets.pop(0)

	def search(self, packet):
		for p in self.packets:
			if len(p) > len(packet):
				for i in range(0, len(packet)):
					if p[i] != packet[i]:
						break
					self.packets.remove(p)
					return p
		return None
