# import the necessary packages
from threading import Thread
import sys
import cv2
import time

# import the Queue class from Python 3
if sys.version_info >= (3, 0):
    from queue import Queue, Full, Empty

# otherwise, import the Queue class for Python 2.7
else:
    from Queue import Queue


class FileVideoStream:

    def __init__(self, path, transform=None, queue_size=128, skip_frames=True, read_timeout=2):
        # initialize the file video stream along with the boolean
        # used to indicate if the thread should be stopped or not
        self.queue_get_timeout = read_timeout
        self.skip_frames = skip_frames
        self.stream = cv2.VideoCapture(path)
        self.total_frames = self.stream.get(cv2.CAP_PROP_FRAME_COUNT)
        self.skipped_frames = 0
        self.stopped = False
        self.transform = transform

        # initialize the queue used to store frames read from
        # the video file
        self.Q = Queue(maxsize=queue_size)
        # initialize thread
        self.thread = Thread(target=self.update, args=(), daemon=True)

    def is_check_eos(self):
        return self.stream.get(cv2.CAP_PROP_POS_FRAMES) >= self.total_frames

    def start(self):
        # start a thread to read frames from the file video stream
        self.thread.start()
        return self

    def get_frame(self):
        # grab the current frame
        flag, frame = self.stream.read()

        while not flag and self.skip_frames:
            if self.is_check_eos():
                return None, None
            if self.skipped_frames == 0:
                print(f"Skipping frame(s)")
            self.skipped_frames += 1
            flag, frame = self.stream.read()
        if self.skipped_frames > 0:
            print(f"Resuming video...")
            self.skipped_frames = 0

        return flag, frame

    def update(self):
        while not self.stopped:
            # read the next frame from the file
            grabbed, frame = self.get_frame()
            # if the `grabbed` boolean is `False`, then we have
            # reached the end of the video file
            if grabbed is None or not grabbed:
                print("Could not grab")
                self.stopped = True
                break

            # if there are transforms to be done, might as well
            # do them on producer thread before handing back to
            # consumer thread. i.e. Usually the producer is so far
            # ahead of consumer that we have time to spare.
            #
            # Python is not parallel but the transform operations
            # are typically OpenCV native so release the GIL.
            #
            # Really just trying to avoid spinning up additional
            # native threads and overheads of additional
            # producer/consumer queues since this one was generally
            # idle grabbing frames.
            if self.transform:
                frame = self.transform(frame)
            while True:
                try:
                    # try to put it into the queue
                    self.Q.put(frame, True, 0.5)
                    break
                except Full:
                    print("Queue is full")
                    if self.stopped:
                        break
        print("Release")
        self.stream.release()

    def dim(self):
        width = int(self.stream.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.stream.get(cv2.CAP_PROP_FRAME_HEIGHT))

        return [width, height]

    def read(self):
        # return next frame in the queue
        try:
            return self.Q.get(timeout=self.queue_get_timeout)
        except Empty:
            return None

        # Insufficient to have consumer use while(more()) which does
        # not take into account if the producer has reached end of
        # file stream.
    def running(self):
        return self.more() or not self.stopped

    def more(self):
        # return True if there are still frames in the queue. If stream is not stopped, try to wait a moment
        tries = 0
        while self.Q.qsize() == 0 and not self.stopped and tries < 5:
            time.sleep(0.1)
            tries += 1

        return self.Q.qsize() > 0

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True
        return self
