# import the necessary packages
import datetime

class FPS:
    def __init__(self):
        """
        store the start time, end time, and total number of frames
        that were examined between the start and end intervals
        """
        self._start = None
        self._end = None
        self._numFrames = 0
        self._pause = False

    def start(self):
        """start the timer"""
        self._start = datetime.datetime.now()
        return self

    def stop(self):
        """stop the timer"""
        self._end = datetime.datetime.now()
        self._pause = True

    def unpause(self, if_not_paused:str = None):
        """
        Unpause the stopped timer.

        Parameters
        ----------
        if_not_paused : str, {None, 'restart', 'raise'} default = None
            This parameter controls behaviour when the timer has not been
            paused:
            ``None``:
                Do nothing.
            ``'restart'``:
                Restart both the timer and the frame counter from zero.
            ``'raise'``:
                Raise an error.
        """
        if self._pause:
            self._start = datetime.datetime.now() - (self._end - self._start)
            self._end = None
            self._pause = False
        elif if_not_paused == 'restart':
            self._end = None
            self._numFrames = 0
            return self.start()
        elif if_not_paused == 'raise':
            raise ValueError('Timer has not been paused.')

    def update(self):
        """
        increment the total number of frames examined during the
        start and end intervals
        """
        if not self._pause:
            self._numFrames += 1

    def elapsed(self):
        """
        return the total number of seconds between the start and
        end interval
        """
        if self._end is None:
            return (datetime.datetime.now() - self._start).total_seconds()
        else:
            return (self._end - self._start).total_seconds()

    def fps(self):
        """compute the (approximate) frames per second"""
        return self._numFrames / self.elapsed()
