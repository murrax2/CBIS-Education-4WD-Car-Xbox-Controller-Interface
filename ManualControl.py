#!/usr/bin/python
import sys
import wiringpi2
from time import sleep

# Test rig for the car
# Author CBiS Education 2012-2015
print '******************************'
print 'CBiS Education - Manual Car Control'
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
wiringpi2.softPwmCreate(ENA,0,100)
wiringpi2.softPwmCreate(ENB,0,100)
wiringpi2.pinMode(IN1,1)
wiringpi2.pinMode(IN2,1)
wiringpi2.pinMode(IN3,1)
wiringpi2.pinMode(IN4,1)

# Number of seconds to pause before programme starts
# Give yourself enough time to unplug the car ready for driving
TimeTillStart = 10
# Loop for 1 second at a time before starting sequences
for x in range(0, 10):
    # Print out an update of how long till the sequence starts
    print "Begin Sequence in %d" % (TimeTillStart-x)
    #pause for 1 second
    sleep(1)


print 'Start of sequence 1'

# Set the direction of the left side
# IN1, 0 IN2, 1 = foward
# IN1, 1 IN2, 0 = backward
wiringpi2.digitalWrite(IN1,0)
wiringpi2.digitalWrite(IN2,1)

# Set the direction of the right side
# IN3, 1 IN4, 0 = foward
# IN3, 0 IN4, 1 = backward
wiringpi2.digitalWrite(IN3,1)
wiringpi2.digitalWrite(IN4,0)

# Set the speed demand of the left
# 0 = 0% speed - 100 = 100% speed
wiringpi2.softPwmWrite(ENA,100)

# Set the speed demand of the right
# 0 = 0% speed - 100 = 100% speed
wiringpi2.softPwmWrite(ENB,100) 

# Set how long to run the sequence for
sleep(5)


# All stop
wiringpi2.softPwmWrite(ENA,0)
wiringpi2.softPwmWrite(ENB,0)
print 'All Stop'
