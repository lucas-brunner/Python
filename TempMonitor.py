import clr
import time
import serial

clr.AddReference(r'C:\Program Files\openhardwaremonitor-v0.9.6\OpenHardwareMonitor\OpenHardwareMonitorLib')

from OpenHardwareMonitor.Hardware import Computer

#/lpc/nct6796dr/control/0 = case fans
#/lpc/nct6796dr/control/1 = cpu fan

# declare constants
MB = 0
CPU = 1
GPU = 2

# declare default variable values
cpuTemp = "--"
gpuTemp = "--"
cpuFan = "--"
gpuFan = "--"
outputData = ""

# establish serial connection to Arduino Nano
ser = serial.Serial('COM3', 115200, timeout=0.050)
time.sleep(2) # wait for connection to finish establishing

# enable readings from CPU, GPU, and motherboard
c = Computer()
c.MainboardEnabled = True
c.CPUEnabled = True
c.GPUEnabled = True
c.Open()

while True:
    time.sleep(2)
    
    print("---------------------------")
    
    # retrieve current CPU sensor readings and if the reading is for temperature, print and store the value
    c.Hardware[CPU].Update()
    for a in range(0, len(c.Hardware[CPU].Sensors)):
        if "/amdcpu/0/temperature/4" in str(c.Hardware[CPU].Sensors[a].Identifier):
            print(c.Hardware[CPU].Sensors[a].get_Value())
            print(c.Hardware[CPU].Sensors[a].Identifier)
            cpuTemp = str(round(c.Hardware[CPU].Sensors[a].get_Value()))
        
    # retrieve current fan controller sensor readings and if the reading is for the CPU fan speed percent, print and store the value
    c.Hardware[MB].SubHardware[0].Update()
    for i in range(0, len(c.Hardware[MB].SubHardware[0].Sensors)):
        if "/lpc/nct6796dr/control/1" in str(c.Hardware[MB].SubHardware[0].Sensors[i].Identifier):
            print(c.Hardware[MB].SubHardware[0].Sensors[i].get_Value())
            print(c.Hardware[MB].SubHardware[0].Sensors[i].Identifier)
            cpuFan = str(round(c.Hardware[MB].SubHardware[0].Sensors[i].get_Value()))
        
    # retrieve current GPU sensor readings and if the reading is for temperature or fan speed percent, print and store the value
    c.Hardware[GPU].Update()
    for b in range(0, len(c.Hardware[GPU].Sensors)):
        if str(c.Hardware[GPU].Sensors[b].SensorType) == "Temperature":
            print(c.Hardware[GPU].Sensors[b].get_Value())
            print(c.Hardware[GPU].Sensors[b].Identifier)
            gpuTemp = str(round(c.Hardware[GPU].Sensors[b].get_Value()))
            
        elif str(c.Hardware[GPU].Sensors[b].SensorType) == "Control":
            print(c.Hardware[GPU].Sensors[b].get_Value())
            print(c.Hardware[GPU].Sensors[b].Identifier)
            gpuFan = str(round(c.Hardware[GPU].Sensors[b].get_Value()))
            
            
    print("---------------------------")
    
    # format the data to be sent to the Arduino. it is expecting "CPUTEMP_CPUFAN_GPUTEMP_GPUFAN"
    outputData = "%s_%s_%s_%s" % (cpuTemp, cpuFan, gpuTemp, gpuFan)
    
    # print the data for debugging purposes
    print(outputData)
    
    # send the data to the Arduino Nano via serial
    ser.write(outputData.encode())
