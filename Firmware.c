#include <RPC.h>

RPC rpc(9600);

void setup() {
	rpc.begin();
	rpc.add_callback(helloWorld_Wrapper, 1);
	rpc.add_callback(printInts_Wrapper, 2);
	delay(1000);
	Serial.println("Arduino RPC Demo");
}

void loop() {
	rpc.check();
}

void helloWorld(){
	Serial.println("Hello World!");
}

void printInts(int a, int b) {
	Serial.print("a: ");
	Serial.println(a);
	Serial.print("b: ");
	Serial.println(b);
}



