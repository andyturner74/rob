# Attach: SR-04 Range finder, switch on SW1, and of course motors.

# The switch SW2 stops and starts the robot

from rrb3 import *
import time, random
import serial

BATTERY_VOLTS = 9
MOTOR_VOLTS = 6

rr = RRB3(BATTERY_VOLTS, MOTOR_VOLTS)

ser = serial.Serial('/dev/ttyACM0', 9600)

# if you dont have a switch, change the value below to True
running = False

distance_left = []
distance_right = []

def backup():
    rr.stop()
    rr.reverse(0.5, 0.33)


def clear_right():
    ser.write('1') # tell arduino to start sweeping sensor left and right
    prev_distance = 5000
    prev_angle = 90

    ser.flushInput()

    prev_save = False

    while True:
        distance = rr.get_distance()
        angle = ser.readline()

        if int(angle) > prev_angle: # scanning left
            if prev_save == False:
                distance_left.append(distance)
        else: # scanning right
            if prev_save == False:
                distance_right.append(distance)
        prev_save = not prev_save
        prev_angle = int(angle)
        time.sleep(0.05)
        if int(angle) < 10: # done scanning
            break

    # get average of distance_right and distance_left
    if len(distance_right) > 0:
        average_right = sum(distance_right) / float(len(distance_right))
    else:
        average_right = 0
        
           
    if len(distance_left) > 0:
        average_left = sum(distance_left) / float(len(distance_left))
    else:
        average_left = 0

    print 'average left len is ' + str(len(distance_left)) + '\n'
    print 'average right len is ' + str(len(distance_right)) + '\n'

    print 'average left is ' + str(average_left) + '\n'
    print 'average right is ' + str(average_right) + '\n'

    if average_right > average_left:
        return True
    else:
        return False

def turn_right():
    rr.right(0.25, 0.25)

def turn_left():
    rr.left(0.25, 0.25)



def turn_randomly():
    turn_time = random.randint(1, 3)
    if random.randint(1, 2) == 1:
        rr.left(turn_time, 0.25) # turn at quarter speed
    else:
        rr.right(turn_time, 0.25)
    rr.stop()

try:
    while True:
        distance = rr.get_distance()
#        print(distance)
        if distance < 50 and running:
            backup()
            if clear_right():
                turn_right()
            else:
                turn_left()

        del distance_right[:]
        del distance_left[:]

        if running:
            rr.forward(3, 0.33)  # set forward speed to 30% of full speed and move forward for 3 seconds
            if clear_right():
                turn_right()
            else:
                turn_left()
        if rr.sw2_closed():
            running = not running
        if not running:
            rr.stop()
        time.sleep(0.2)
finally:
    print("Exiting")
    rr.cleanup()
    
