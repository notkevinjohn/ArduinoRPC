#include "Arduino.h"

/*Kevin John 2024. Remote Procedure Call Library for Arduino --> Python */

#ifndef RPC_h
#define RPC_h

class RPC
{
	public:
		RPC(int baudRate);
		void begin();
		void check();
		void add_callback(void(*fp)(byte[]), int packetType);
		void appendCharToPacketOut(char value);
		void appendByteToPacketOut(byte value);
		void appendIntToPacketOut(int value);

	private:
		int readPacket();
		void processPacket(byte packetType);
		void writePacket(struct packet);
		void unassigned(int args[]);
		void writePacketOut();
		void confirmPacket(byte recognized);
		void responsePacket(byte packetType, int value);
		void clearPacketOut();
		void clearPacketIn();
		void clearPacketInBytes();
};

#endif
