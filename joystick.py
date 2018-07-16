import pygame
import sys
import time
import threading
import stream_server
import easygopigo3 as easy

class JoyStatus:
    def __init__(self):
        self.direction = (0, 0)
        self.accelerate = False
        self.bark = False

def control_gopigo(robot, joystatus):
    moving = False
    prev_speed = robot.get_speed() // 50
    while True:
        d = joystatus.direction
        print "d={}".format(d)
        if d[1] < 0 or d[1] > 0:
            speed = int(abs(d[1]) * 6) + 1
            print "speed={}, prev_speed={}".format(speed, prev_speed)
            if (speed != prev_speed):
                print "Setting speed to {}".format(speed)
                robot.set_speed(speed * 50)
                prev_speed = speed

        if d != (0, 0) and not moving:
            moving = True
            if d[1] < 0 :
                print "Driving robot forward"
                robot.forward()
            elif d[1] > 0 :
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
robot.set_left_eye_color((0, 255, 0))
robot.open_left_eye()
pygame.init()

pygame.joystick.init()

js_count = pygame.joystick.get_count()
print "Found {} joysticks".format(js_count)
if (js_count == 0):
    sys.exit()
joystatus = JoyStatus()

video_thread = None

clock = pygame.time.Clock()
robot.set_right_eye_color((0, 255, 0))
robot.open_right_eye()
streaming_cv = None
b1_pressed = 0
while (True):
    clock.tick(10)
    pygame.event.get()
    js = pygame.joystick.Joystick(0)
    js.init()
    joystatus.direction = (js.get_axis(0), js.get_axis(1))
    if js.get_button(1):
        if video_thread is None or not video_thread.is_alive():
            print "Starting video"
            robot.close_eyes()
            robot.set_eye_color((255, 0, 0))
            robot.open_eyes()
            video_thread = threading.Thread(target = stream_server.start)
            video_thread.start()

