import serial, time
arduino = serial.Serial('/dev/ttyACM0', 115200, timeout=.1)
time.sleep(4) #give the connection a second to settle
arduino.write("Hello from Python!")
while True:
	data = arduino.readline()
	if data:
		print data.rstrip('\n') #strip out the new lines for now
