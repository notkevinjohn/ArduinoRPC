#include <RPC.h> //added automatically

RPC rpc(115200); //added automatically

void setup() {
	rpc.begin(); //added automatically
	register_callbacks(); //added automatically
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

int addInts(int a, int b) {
	return a+b;
}




