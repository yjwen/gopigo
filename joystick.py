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
    moving = False
    while True:
        d = joystatus.direction
        if d != (0, 0) and not moving:
            moving = True
            if d[1] > 0 :
                print "Driving robot forward"
                robot.forward()
            elif d[1] < 0 :
                print "Driving robot backward"
                robot.backward()
            elif d[0] > 0:
                print "Turning robot right"
                robot.right()
            elif d[0] < 0:
                print "Turning robot left"
                robot.left()
        elif d == (0, 0) and moving:
            moving = False
            robot.stop()

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
robot.set_right_eye_color((255, 0, 0))
robot.open_right_eye()
while (True):
    clock.tick(10)
    pygame.event.get()
    js = pygame.joystick.Joystick(0)
    js.init()
    joystatus.direction = js.get_hat(0)


            
    
    
