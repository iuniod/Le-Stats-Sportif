from queue import Queue
from threading import Thread, Event, Lock
import time
import os

class ThreadPool:
    def __init__(self):
        """ Initialize the ThreadPool. """
        self.num_threads = self.get_num_threads()
        self.task_queue = Queue()
        self.tasks = []
        self.lock = Lock()

    def start(self):
        """ Start the thread pool: create and run the threads."""
        for _ in range(self.num_threads):
            task_runner = TaskRunner(self.task_queue, self.lock)
            task_runner.start()
            self.tasks.append(task_runner)

    def join(self):
        """ Wait for all threads to finish and join them. """
        for task in self.tasks:
            task.shutdown.set()
        
        for task in self.tasks:
            task.join()


    def get_num_threads_from_env_var(self):
        """
        Check if an environment variable TP_NUM_OF_THREADS is defined.
        If the env var is defined, return that value.
        Otherwise, return None.
        """
        return os.environ.get('TP_NUM_OF_THREADS', None)

    def get_num_threads(self):
        """
        Check if an environment variable TP_NUM_OF_THREADS is defined.
        If the env var is defined, that is the number of threads to be used by the thread pool.
        Otherwise, you are to use what the hardware concurrency allows.
        """
        num_threads = self.get_num_threads_from_env_var()
        return os.cpu_count() if num_threads is None else int(num_threads)


class TaskRunner(Thread):
    def __init__(self, task_queue, lock):
        super().__init__()
        self.task_queue = task_queue
        self.shutdown = Event()
        self.lock = lock

    def run(self):
        """ Run task as long as the shutdown event is not set. """
        while not self.shutdown.is_set():
            # get the task from the queue, if available and execute it
            self.lock.acquire()

            if not self.task_queue.empty():
                task_to_exec = self.task_queue.get()
                self.lock.release()
                self.execute_task(task_to_exec)
            else:
                self.lock.release()
    
    def execute_task(self, task):
        print(f"Executing task: {task}")
