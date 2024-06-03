#!/usr/bin/python3
from ArduinoSketchParser import ArduinoSketchParser
from InterfaceGenerator import InterfaceGenerator
from PythonClassExporter import PythonClassExporter

#device = "/dev/arduino-mega"
sketchData = ArduinoSketchParser("Firmware.c").parse()
print (sketchData)
#interface = InterfaceGenerator(sketchData).writeFile("Interface.txt")
#exporter = PythonClassExporter(sketchData, device)


