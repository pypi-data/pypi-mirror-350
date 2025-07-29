import sys
import time

class RunningIndicator:
    '''
    This class provides an indication for running while loops. Gives information about time passed but cant make
    estimations about time left and progress done
    just call this object at the beginning of each loop
    '''
    def __init__(self, mode='dots', update_frq = 1):
        self._state = 0 # which state of the charset gets printed at update time
        self._formatter = "Running %s | AVG loop time: %.2f sec| time passed: %.2f sec"  # the formatter string to print each update
        self._update_frq = update_frq # the amount of loops to pass before the output gets updated

        # select the given charset
        if mode == 'dots':
            self._chars = ['.  ', '.. ', '...']
        elif mode == 'rotate':
            self._chars = ['- ', '\ ', '/ ']
        else:
            raise ValueError('{} is not a valid mode'.format(mode))

        # properties for timing
        self._start_time = time.time()  # saves the start time
        self._time_elapsed = 0
        self._iter = 0

    def __call__(self):
        self._iter += 1 # count passed iters
        if self._iter == 1:
            self._time_elapsed = time.time() - self._start_time  # update elapsed time
            self._avg_iter_time = self._time_elapsed / self._iter  # update average time per loop

            sys.stdout.write('\r')  # resets the cursor
            sys.stdout.write(
                self._formatter % (self._chars[self._state], self._avg_iter_time, self._time_elapsed))  # prints the msg
            sys.stdout.flush()

            # update internal state
            self._state += 1

        if self._iter % self._update_frq == 0: # check if frq time is met
            self._time_elapsed = time.time() - self._start_time  # update elapsed time
            self._avg_iter_time = self._time_elapsed / self._iter  # update average time per loop

            sys.stdout.write('\r')  # resets the cursor
            sys.stdout.write(self._formatter % (self._chars[self._state], self._avg_iter_time, self._time_elapsed)) # prints the msg
            sys.stdout.flush()

            # update internal state
            self._state += 1
            if self._state == 3:
                self._state = 0
