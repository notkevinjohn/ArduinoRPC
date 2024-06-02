#include "Arduino.h"
#include "RPC.h"

int _baudRate;
char packetIn[48];
char packetOut[48];
int packetIndexIn;
int packetIndexOut;
int packetInBytesIndex;
byte packetInBytes[24];


void (*callbacks[255]) (byte[]);

void RPC::add_callback(void (*fp)(byte[]), int packetType){
	callbacks[packetType]  = fp;
}

RPC::RPC(int baudRate){
	_baudRate = baudRate;
	for (int i = 0; i<255; i++){
		callbacks[0] = 0;
	}
	RPC::clearPacketIn();
	RPC::clearPacketOut();
}

void RPC::begin() {
	Serial.begin(_baudRate);
	while (!Serial) { delay(1); }
}

void RPC::check() {
	if(Serial.available() > 0 ){
                byte packetType =  readPacket();
		processPacket(packetType);
        }
}

char byteChars[3];
int RPC::readPacket() {
        packetIndexIn = Serial.readBytesUntil('\n', packetIn, 48);
	packetInBytesIndex=0;
	for (int i =0; i < packetIndexIn; i+=2) {
		byteChars[0] = (char)packetIn[i];
		byteChars[1] = (char)packetIn[i+1];
		byteChars[2] =  NULL;
		byte packetByte = strtoul(byteChars, NULL, 16);
		packetInBytes[packetInBytesIndex] = packetByte;
		packetInBytesIndex +=1;
	}
	return packetInBytes[0];
}

void RPC::processPacket(byte packetType) {
	byte args[packetIndexIn-1];
	for (int i = 1; i<packetInBytesIndex; i++){
		args[i-1] = packetInBytes[i];
	}
	if (callbacks[packetType] != 0){
		RPC::confirmPacket(1);
		(*callbacks[packetType])(args);
	}
	else {
		RPC::confirmPacket(0);
	}

}

void RPC::clearPacketInBytes() {
        for(int i=0; i<=24; i++){
                packetInBytes[i] = 0;
        }
}

void RPC::clearPacketIn() {
        for(int i=0; i<=48; i++){
                packetIn[i] = 0;
        }
        packetIndexIn = 0;
}

void RPC::clearPacketOut() {
        for(int i=0; i<=48; i++){
                packetOut[i] = 0;
        }
        packetIndexOut = 0;
}

void RPC::appendCharToPacketOut(char value){
        packetOut[packetIndexOut]=value;
        packetIndexOut++;
}

char byteBuffer[2];
void RPC::appendByteToPacketOut(byte value){
	sprintf(byteBuffer, "%02X", value);
	RPC::appendCharToPacketOut(byteBuffer[0]);
	RPC::appendCharToPacketOut(byteBuffer[1]);
}

char intBuffer[4];
void RPC::appendIntToPacketOut(int value){
	sprintf(intBuffer, "%04X", value);
	RPC::appendCharToPacketOut(intBuffer[0]);
	RPC::appendCharToPacketOut(intBuffer[1]);
	RPC::appendCharToPacketOut(intBuffer[2]);
	RPC::appendCharToPacketOut(intBuffer[3]);
}

void RPC::confirmPacket(byte recognized) {
	RPC::appendByteToPacketOut(0);
 	for (int i=0; i<packetIndexIn; i++){
               RPC::appendCharToPacketOut(packetIn[i]);
        }
	RPC::appendByteToPacketOut(recognized);
        RPC::writePacketOut();
}

void RPC::writePacketOut(){
        int i = 0;
        for (i=0; i<packetIndexOut; i++){
                Serial.print(packetOut[i]);
        }
        Serial.print('\n');
        RPC::clearPacketOut();
}


