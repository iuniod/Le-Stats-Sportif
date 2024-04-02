from queue import Queue
from threading import Thread, Event, Lock
from app.job import Job
import time
import os

class ThreadPool:
    def __init__(self):
        """ Initialize the ThreadPool. """
        self.num_threads = self.get_num_threads()
        self.job_queue = Queue()
        self.job_list = []
        self.tasks = []
        self.lock = Lock()
        self.data_ingestor = None

    def start(self, data_ingestor):
        """ Start the thread pool: create and run the threads."""
        self.data_ingestor = data_ingestor
        for _ in range(self.num_threads):
            task_runner = TaskRunner(self.job_queue, self.lock, self.data_ingestor)
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

    def register_job(self, job_id, data, type_command):
        """ Register a job and add task to the task queue."""
        job = Job(job_id, data, type_command)

        self.lock.acquire()
        self.job_queue.put(job)
        self.job_list.append(job)
        self.lock.release()


class TaskRunner(Thread):
    def __init__(self, job_queue, lock, data_ingestor):
        super().__init__()
        self.job_queue = job_queue
        self.shutdown = Event()
        self.lock = lock
        self.data_ingestor = data_ingestor

    def run(self):
        """ Run task as long as the shutdown event is not set. """
        while not self.shutdown.is_set():
            # get the task from the queue, if available and execute it
            self.lock.acquire()

            if not self.job_queue.empty():
                job = self.job_queue.get()
                self.lock.release()
                job.run(self.data_ingestor)
            else:
                self.lock.release()
