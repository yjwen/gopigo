import socket
import time
import picamera

def start(robot = None):
    if robot is not None:
        robot.set_left_eye_color((255, 0, 0))
    camera = picamera.PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 24

    server_socket = socket.socket()
    server_socket.bind(('0.0.0.0', 8000))
    server_socket.listen(0)
    if robot is not None:
        robot.set_right_eye_color((255, 0, 0))
    connection = server_socket.accept()[0].makefile('wb')
    try:
        camera.start_recording(connection, format='h264')
        camera.wait_recording(600)
        camera.stop_recording()
    finally:
        connection.close()
        server_socket.close()
        if robot is not None:
            robot.set_eye_color((0, 255, 0))

