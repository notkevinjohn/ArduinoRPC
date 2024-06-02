void helloWorld_Wrapper(byte args[]){
	helloWorld();
}

struct  printInts_Inputs {
	byte a;
	byte b;
};

void printInts_Wrapper(byte args[]){
	printInts_Inputs inputs;
	memcpy(&inputs, args, 2);
	printInts(inputs.a, inputs.b);
	//rpc.appendIntToPacketOut(inputs.value);
}




