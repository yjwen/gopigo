import socket
import time
import picamera
import threading

def test_send_stream(robot, cv):
    cv.acquire()
    print "Streaming"
    cv.wait()
    print "Streaming ends."
    cv.release()

# Connect a client socket to my_server:8000 (change my_server to the
# hostname of your server)
def send_stream(robot, cv):
    robot.set_left_eye_color((255, 0, 0))
    # cv.acquire()

    client_socket = socket.socket()
    client_socket.connect(('192.168.0.100', 8000))
    robot.set_right_eye_color((255, 0, 0))
    try:
        # Make a file-like object out of the connection
        connection = client_socket.makefile('wb')
        camera = picamera.PiCamera()
        camera.resolution = (640, 480)
        camera.framerate = 24
        # Start a preview and let the camera warm up for 2 seconds
        camera.start_preview()
        time.sleep(2)
        # Start recording, sending the output to the connection for 60
        # seconds, then stop
        camera.start_recording(connection, format='h264')
        # cv.wait()
        camera.wait_recording(0)
        camera.stop_recording()
    finally:
        connection.close()
        client_socket.close()
        # cv.release()

    robot.set_eye_color((0, 255, 0))

def receive_stream():
    # Start a socket listening for connections on 0.0.0.0:8000 (0.0.0.0 means
    # all interfaces)
    server_socket = socket.socket()
    server_socket.bind(('0.0.0.0', 8000))
    server_socket.listen(0)
    print "Listening"
    # Accept a single connection and make a file-like object out of it
    connection = server_socket.accept()[0].makefile('rb')
    print "Connected."
    try:
        # Run a viewer with an appropriate command line. Uncomment the mplayer
        # version if you would prefer to use mplayer instead of VLC
        cmdline = ['vlc', '--demux', 'h264', '-']
        #cmdline = ['mplayer', '-fps', '25', '-cache', '1024', '-']
        player = subprocess.Popen(cmdline, stdin=subprocess.PIPE)
        print "Pipe opened."
        while True:
            # Repeatedly read 1k of data from the connection and write it to
            # the media player's stdin
            data = connection.read(1024)
            if not data:
                break
            player.stdin.write(data)
    finally:
        connection.close()
        server_socket.close()
        player.terminate()

if __name__ == "__main__":
    while True:
        receive_stream()
