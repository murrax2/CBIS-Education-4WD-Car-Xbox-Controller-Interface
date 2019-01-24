#!/usr/bin/python
import socket
import sys
import wiringpi2
from time import sleep

# Test rig for the car
# Author CBiS Education 2012 - 2015
print '******************************'
print 'CBiS Education - 4WD Remote Control Car '
print ''

# black wire to BCM GPIO 6 row 2 pin 3 for ground (0v)

# PORTA Motors on left side of car
ENA = 0 # RPi 11 - row 1 pin 6
IN1 = 1 # RPi 12 - row 2 pin 6
IN2 = 2 # RPi 13 - row 1 pin 7

# PORTB Motors on right side of car
ENB = 3 # RPi 15 - row 1 pin 8
IN3 = 4 # RPi 16 - row 2 pin 8
IN4 = 5 # RPi 18 - row 2 pin 9

# Configure the GPIO Pins on the Pi 
# to control the Motor shield
wiringpi2.wiringPiSetup()
wiringpi2.softPwmCreate(ENA,0,250)
wiringpi2.softPwmCreate(ENB,0,250)
wiringpi2.pinMode(IN1,1)
wiringpi2.pinMode(IN2,1)
wiringpi2.pinMode(IN3,1)
wiringpi2.pinMode(IN4,1)

HOST = ''
PORT = 5000

# Setup a Datagram (udp) socket to receive commands over the network
try :
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print 'Socket created'
except socket.error, msg :
        print 'Failed to create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()


# Bind socket to local host and port
try:
        s.bind((HOST, PORT))
except socket.error , msg:
        print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()
        
print 'Socket bind complete'
print ''
print 'Ready to receive remote control commands...'

# Car Control From Commands
while 1:
        # receive data from computer application (data, addr)
        d = s.recvfrom(1024)
        data = d[0]
        addr = d[1]

        if not data: 
                break        

        # check to see if command is release
        if data == 'RELEASE':
                wiringpi2.softPwmWrite(ENA,0)
                wiringpi2.softPwmWrite(ENB,0)
        else:
                # hopefully command is a car control else there is an error
                command = data.replace("C:","")
                commandvrs = command.split("|",1)
                leftcommand = int(commandvrs[0])
                rightcommand = int(commandvrs[1])
                
				# Define the direction of the motors
                if leftcommand < 0:                        
						# Left motors backwards
                        leftcommand = int(str(leftcommand).replace("-",""))                        
                        wiringpi2.digitalWrite(IN1,1)
                        wiringpi2.digitalWrite(IN2,0)                        
                else:
						#Left motors forwards
                        wiringpi2.digitalWrite(IN1,0)
                        wiringpi2.digitalWrite(IN2,1)

                if rightcommand < 0:
						# Right motors backwards
                        rightcommand = int(str(rightcommand).replace("-",""))                        
                        wiringpi2.digitalWrite(IN3,0)
                        wiringpi2.digitalWrite(IN4,1)
                else:
                        # Right motors forwards
                        wiringpi2.digitalWrite(IN3,1)
                        wiringpi2.digitalWrite(IN4,0)

				# Velocity demand - how fast
                wiringpi2.softPwmWrite(ENA,leftcommand)
                wiringpi2.softPwmWrite(ENB,rightcommand) 
        
        # Uncomment the below to see the commands being received
        # print 'Message[' + addr[0] + ':' + str(addr[1]) + '] - ' + data.strip()

s.close()
