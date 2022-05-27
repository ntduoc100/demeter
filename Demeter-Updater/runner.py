'''
This script create threads for each modules
which are used to handle data from different data sources

When adding more modules, add code in all EDIT HERE blocks below
'''

import threading as th
import signal
from datetime import datetime
import time

# Import updaters here
from openweathermap.updater import UpdaterRealtime, UpdaterInterval


class Job(th.Thread):
    '''
    Description:
    - Create thread job that run forever
    '''

    def __init__(self, name, worker, runner, interval=0.5, **kwargs):
        '''
        Parameters:
        - worker: function where the code should be run in the thread
        - interval: amount of time between executions
        - runner: function that wrap the worker with additional code
        '''
        th.Thread.__init__(self)

        self.shutdown_flag = th.Event()
        self.worker = worker
        self.interval = interval
        self.runner = runner
        self.kwargs = kwargs
        self.name = name

    def run(self):
        while not self.shutdown_flag.is_set():
            # Job code
            self.runner(self.worker, self.interval, **self.kwargs)


class ServiceExit(Exception):
    """
    Custom exception which is used to trigger the clean exit
    of all running threads and the main program.
    """
    pass


def service_shutdown(signum, frame):
    '''Raise exception to stop the program when a terminate signal received'''
    raise ServiceExit


# These functions are used to wrap up worker functions
# and define the behaviors of each thread

# Each function must have worker, interval as their parameters
######################################################
# EDIT HERE

def interval_runner(worker, interval, **kwargs):
    '''Only start at minute 0 or 30'''
    cur_min, cur_sec = datetime.now().strftime(r'%M-%S').split('-')
    if (cur_min == '00' or cur_min == '30') and int(cur_sec) <= 0.5:
        worker(kwargs['collname'])


def realtime_runner(worker, interval, **kwargs):
    '''Collect data, keep the interval accuracy'''
    worker(kwargs['collname'])
    time.sleep(interval)

# END OF EDIT
######################################################

if __name__ == '__main__':
    

    connection_str = 'mongodb+srv://root:12345ADMIN@cluster0.5qjhz.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'
    ###############################################
    # Testing 
    # connection_str = 'mongodb://demeterdb:27017'
    ###############################################

    # This below part is used to created threads for parallel
    # realtime and interval processes
    

    # Add updater objects
    ######################################################
    # EDIT HERE

    realtime_object = UpdaterRealtime(connection_str, 'demeter')
    interval_object = UpdaterInterval(connection_str, 'demeter')

    # END OF EDIT
    ######################################################


    # Register signals
    signal.signal(signal.SIGTERM, service_shutdown)
    signal.signal(signal.SIGINT, service_shutdown)

    try:
        # Define thread for each objects
        ######################################################
        # EDIT HERE
        realtime = Job(
            'realtime',
            realtime_object.update,
            realtime_runner,
            300, # Change this to change the time between api calls for real time
            collname='realtime_data'
        )

        interval_30 = Job(
            'interval',
            interval_object.update,
            interval_runner,
            0,
            collname='historical_data'
        )

        # Start the threads
        realtime.start()
        interval_30.start()

        # END OF EDIT
        ######################################################
        # Keep the program alive
        while True:
            time.sleep(0.5)

    except ServiceExit:

        # Shutdown threads
        ######################################################
        # EDIT HERE

        realtime.shutdown_flag.set()
        interval_30.shutdown_flag.set()

        # Wait for the threads to close...
        realtime.join()
        interval_30.join()

        # END OF EDIT
        ######################################################
