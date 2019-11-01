"""
This module contains a Camera class, whose objects are distinguished by the input they capture.
The metaphor is a bit confusing becasue the real process contains no actual camera, but think of
the generator passed to the constructor as the actual 'camera', i.e. the thing that provides data.
The rest of the object is like a driver which notifies clients when frames are available.

The code is a modified version of a demonstration on video streaming in Flask, which also explains
the camera idea, since that project actually streams a camera feed:
    https://github.com/miguelgrinberg/flask-video-streaming/tree/v1
That project contains the asynchronous handling, largely unchanged here.
"""


from cv2 import imencode
import time
import threading
try:
    from greenlet import getcurrent as get_ident
except ImportError:
    try:
        from thread import get_ident
    except ImportError:
        from _thread import get_ident


class CameraEvent(object):
    def __init__(self):
        self.events = {}

    def wait(self):
        ident = get_ident()
        if ident not in self.events:
            self.events[ident] = [threading.Event(), time.time()]
        return self.events[ident][0].wait()

    def set(self):
        now = time.time()
        remove = None
        for ident, event in self.events.items():
            if not event[0].isSet():
                event[0].set()
                event[1] = now
            else:
                if now - event[1] > 5:
                    remove = ident
        if remove:
            del self.events[remove]

    def clear(self):
        self.events[get_ident()][0].clear()


class Camera(object):
    """ Obviously """ 

    def __init__(self, input, fps=None):
        self.input          = input                                     # A generator of input data; expects numpy arrays of pixels.
        self.fps            = fps                                       # Intended frame rate.

        self.thread         = None                                      # Background thread that reads frames from camera.
        self.frame          = None                                      # Current frame is stored here by background thread.
        self.last_access    = 0                                         # Time of last client access to camera.
        self.event          = CameraEvent()
        # self.poke()                                                   
        
    def poke(self):
        """ Wake the camera up. """
        if self.thread is None:                                         # If the camera is inactive:
            self.last_access = time.time()
            self.thread = threading.Thread(target=self._thread)         # Start colecting input.
            self.thread.daemon = True
            self.thread.start()

            while self.get_frame() is None:                             # Wait until frames are available.
                time.sleep(0)

    def get_frame(self):
        """ Return the current camera frame. """
        self.last_access = time.time()
        self.event.wait()                                              # Wait for signal from the event ('New frame is ready')
        self.event.clear()
        return self.frame

    def frames(self):
        """" Translate camera input into readable format. Like a driver if it were an actual camera. """
        for img in self.input(360, 720, fps=self.fps):
            ret, frame = imencode('.jpg', img)
            yield frame.tobytes()

    def _thread(self):
        """ Collect input. """
        # print(f'Starting camera thread {self.thread.ident}')
        for frame in self.frames():
            self.frame = frame
            self.event.set()                                            # Send signal to clients
            time.sleep(0)

            if time.time() - self.last_access > 3:                      # If nobody has asked for a frame shut it down.
                # print(f'Stopping camera thread {self.thread.ident} due to inactivity.')
                break
        self.thread = None





# Dev functions.
#   Each takes a generator of pixel arrays.

def browser(gen):
    from flask import Flask, Response
    from cv2 import imencode
    from base_camera import BaseCamera

    height, width = 360, 720

    class Camera(BaseCamera):
        @staticmethod
        def frames():
            for img in gen(360, 720):
                ret, frame = imencode('.jpg', img)
                yield frame.tobytes()

    def jpeg(camera):
        while True:
            frame = camera.get_frame()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    app = Flask(__name__)

    @app.route('/')
    def response():
        return Response(jpeg(Camera()),
                        mimetype='multipart/x-mixed-replace; boundary=frame')

    app.run(host='0.0.0.0')


def cv(gen):
    import cv2

    height, width = 360, 720
    w = cv2.namedWindow("win")

    for frame in gen(height, width, 0.005):
        cv2.imshow('win', frame)
        if cv2.waitKey(int(1000/60)) != -1:
            break
            
    cv2.destroyAllWindows()
