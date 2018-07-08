import pygame
import sys
import time
import thread

class JoyStatus:
    def __init__(self):
        self.direction = (0, 0)
        self.accelerate = False
        self.bark = False

def control_gopigo(joystatus):
    while True:
        time.sleep(0.5)
        if joystatus.direction != (0, 0):
            print "GoPiGo: Moving to {}".format(joystatus.direction)

pygame.init()

pygame.joystick.init()

js_count = pygame.joystick.get_count()
print "Found {} joysticks".format(js_count)
if (js_count == 0):
    sys.exit()
joystatus = JoyStatus()

thread.start_new_thread(control_gopigo, (joystatus,))

clock = pygame.time.Clock()
count = 0
while (True):
    clock.tick(1)
    print "Count={}".format(count)
    pygame.event.get()
    js = pygame.joystick.Joystick(0)
    js.init()
    for i in range(js.get_numaxes()):
        axis = js.get_axis(i)
        print("Axis {} value: {:>6.3f}".format(i, axis))
    for i in range(js.get_numbuttons()):
        button = js.get_button(i)
        print "Button {:>2} value: {}".format(i, button)
    joystatus.direction = js.get_hat(0)
    print joystatus.direction
    count = count + 1

sys.exit()

            
    
    
