# pysight.py
"""
Wrapper of the PySight wrapper.
Provides convenience functions on top of PySight, so that no one has to
call ObjC wrappers directly.
"""

from PySight import CSGCamera
from Foundation import NSObject
from PyObjCTools import AppHelper

class Pixel(object):
    """
    A horribly inefficient pixel.
    For real processing, you're going to want to access the buffer in the
    Frame directly.  This is provided just for the option.
    """
    def __init__(self, r, g, b, a):
        self.red, self.green, self.blue = ord(r), ord(g), ord(b)
        self.alpha = ord(a)

    def __repr__(self):
        return "<Pixel(%d,%d,%d,%d)>" % (self.red, self.green, self.blue,
                                         self.alpha)

class Frame(object):
    """
    A Frame contains the bitmap buffer produced by a Camera, and the size
    of the camera.
    """
    def __init__(self, buffer, size):
        assert len(buffer) == size[0]*size[1]*4
        self.bitmap = buffer
        self.size = size
        self.width, self.height = size

    def __getitem__(self, point):
        x, y = point
        assert 0 <= x < self.width and 0 <= y < self.height
        offset = x + y * self.width
        return Pixel(*self.bitmap[offset*4:(offset+1)*4])

    def __repr__(self):
        return "<Frame(..., (%d, %d))>" % self.size


class Camera(object):
    def __init__(self, size=(160,120)):
        self.camera = CSGCamera.alloc().init()
        self.camera.startWithSize_(size)
        self.size = size

    class _GetFrameDelegate(NSObject):
        def camera_didReceiveFrame_(self, camera, frame):
            print "Got a frame!"
            self.frame = frame
            stop_event_loop()

    def get_ns_frame(self):
        """
        Returns a single frame.  This frame is the NSObject frame returned
        by the CSGCamera.
        """
        delegate = Camera._GetFrameDelegate.alloc().init()
        self.camera.setDelegate_(delegate)
        start_event_loop()
        frame = delegate.frame
        self.camera.setDelegate_(None)
        return frame

    def get_frame(self):
        """
        Get a single frame from the camera, and return control immediately.
        """
        frame = self.get_ns_frame()
        imageRep = frame.representations()[0]
        bitmap = imageRep.bitmapData()
        return Frame(bitmap[:], self.size)

    class _CallbackDelegate(NSObject):
        def camera_didReceiveFrame_(self, camera, frame):
            imageRep = frame.representations()[0]
            bitmap = imageRep.bitmapData()
            self.callback( Frame(bitmap, self.size) )

    def callback_loop(self, callback):
        """
        Starts a callback-loop, processing frames as they're produced by
        the camera.  Runs until someone, somewhere, calls stop_event_loop.
        callback should take a single Frame as a parameter.
        """
        delegate = Camera._CallbackDelegate.alloc().init()
        delegate.callback = callback
        delegate.size = self.size
        self.camera.setDelegate_(delegate)
        start_event_loop()
        self.camera.setDelegate_(None)

    def stop(self):
        self.camera.stop()


def start_event_loop():
    AppHelper.runConsoleEventLoop(installInterrupt=True)

def stop_event_loop():
    AppHelper.stopEventLoop()

