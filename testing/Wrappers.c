void register_callbacks(){
	rpc.add_callback(helloWorld_Wrapper, 1);
	rpc.add_callback(printInts_Wrapper, 2);
	rpc.add_callback(addInts_Wrapper, 3);
}

void helloWorld_Wrapper(byte args[]){
	helloWorld();
}

struct printInts_Inputs {
	byte a;
	byte b;
};

void printInts_Wrapper(byte args[]){
	printInts_Inputs inputs;
	memcpy(&inputs, args, 2);
	printInts(inputs.a, inputs.b);
}

struct addInts_Inputs {
	byte a;
	byte b;
};

void addInts_Wrapper(byte args[]){
	addInts_Inputs inputs;
	memcpy(&inputs, args, 2);
	int sum = addInts(inputs.a, inputs.b);
	rpc.appendByteToPacketOut(3);
	rpc.appendIntToPacketOut(sum);
	rpc.writePacketOut();

}






