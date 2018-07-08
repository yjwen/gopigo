import pygame
import sys
import time
import thread
import easygopigo3 as easy

class JoyStatus:
    def __init__(self):
        self.direction = (0, 0)
        self.accelerate = False
        self.bark = False

def control_gopigo(robot, joystatus):
    while True:
        d = joystatus.direction
        if d != (0, 0):
            if d[1] != 0:
                print "Driving robot {}".format(d[1])
                robot.drive_degrees(d[1] * 10)
                print "Done"
            elif d[0] != 0:
                print "Turning robot {}".format(d[0])
                robot.turn_degrees(d[0] * 5)
                print "Done"
        else:
            time.sleep(0.5)


robot = easy.EasyGoPiGo3()
robot.close_eyes()
robot.set_left_eye_color((255, 0, 0))
robot.open_left_eye()
pygame.init()

pygame.joystick.init()

js_count = pygame.joystick.get_count()
print "Found {} joysticks".format(js_count)
if (js_count == 0):
    sys.exit()
joystatus = JoyStatus()

thread.start_new_thread(control_gopigo, (robot, joystatus))

clock = pygame.time.Clock()
count = 0
robot.set_right_eye_color((255, 0, 0))
robot.open_right_eye()
while (True):
    clock.tick(1)
    print "Count={}".format(count)
    pygame.event.get()
    js = pygame.joystick.Joystick(0)
    js.init()
    joystatus.direction = js.get_hat(0)
    count = count + 1

sys.exit()

            
    
    
