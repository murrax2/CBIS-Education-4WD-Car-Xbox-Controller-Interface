#!/usr/bin/python
import sys
import wiringpi2
from time import sleep

# Test rig for the car
# Author CBiS Education 2014
print '******************************'
print 'CBiS Education - Car Test '
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

print 'hey'

# Configure the GPIO Pins on the Pi 
# to control the Motor shield
wiringpi2.wiringPiSetup()
print '1'
wiringpi2.softPwmCreate(ENA,0,250)
print '2'
wiringpi2.softPwmCreate(ENB,0,250)
print '3'
wiringpi2.pinMode(IN1,1)
print '4'
wiringpi2.pinMode(IN2,1)
print '5'
wiringpi2.pinMode(IN3,1)
print '6'
wiringpi2.pinMode(IN4,1)
print '7'

print 'Test Rig Ready'
print 'Test run in 3 seconds'
sleep(1)
print 'Test run in 2 seconds'
sleep(1)
print 'Test run in 1 second'
sleep(1)
print '***** Test has begun *****'
print ''

# Left side forward
print 'Left side forward max power'
wiringpi2.digitalWrite(IN1,0)
wiringpi2.digitalWrite(IN2,1)
wiringpi2.softPwmWrite(ENA,250)
sleep(2)
wiringpi2.softPwmWrite(ENA,0)
sleep(1)
print 'Left side backward max power'
wiringpi2.digitalWrite(IN1,1)
wiringpi2.digitalWrite(IN2,0)
wiringpi2.softPwmWrite(ENA,250)
sleep(2)
wiringpi2.softPwmWrite(ENA,0)
print 'Left test complete'
sleep(1)

# right side forward
print 'Right side forward max power'
wiringpi2.digitalWrite(IN3,1)
wiringpi2.digitalWrite(IN4,0)
wiringpi2.softPwmWrite(ENB,250)
sleep(2)
wiringpi2.softPwmWrite(ENB,0)
sleep(1)
print 'Right side backward max power'
wiringpi2.digitalWrite(IN3,0)
wiringpi2.digitalWrite(IN4,1)
wiringpi2.softPwmWrite(ENB,250)
sleep(2)
wiringpi2.softPwmWrite(ENB,0)
print 'Right test complete'

print 'All testing complete'
