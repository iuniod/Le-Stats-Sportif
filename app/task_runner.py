""" This module contains the ThreadPool and TaskRunner classes for multi-threading. """
from queue import Queue
from threading import Thread, Event, Lock
import os
from app.job import Job

class ThreadPool:
    """ ThreadPool class is a pool of threads that execute tasks from the job_queue. """
    def __init__(self):
        """ Initialize the ThreadPool. """
        self.job_queue = Queue()
        self.job_list = []
        self.tasks = []
        self.lock = Lock()
        self.data_ingestor = None
        self.accepting_jobs = True
        self.logger = None

    def start(self, data_ingestor, logger):
        """ Start the thread pool: create and run the threads."""
        num_threads = self.get_num_threads()
        self.logger = logger
        self.logger.info(f"Starting ThreadPool with {num_threads} threads")
        self.data_ingestor = data_ingestor
        for _ in range(num_threads):
            task_runner = TaskRunner(self.job_queue, self.lock, self.data_ingestor)
            task_runner.start()
            self.tasks.append(task_runner)

    def stop(self):
        """ Don't accept new tasks and wait for the current tasks to finish."""
        self.accepting_jobs = False

        for task in self.tasks:
            task.shutdown.set()
        self.logger.info("Sent shutdown signal to all tasks")

        for task in self.tasks:
            task.join()
        self.logger.info("All tasks have stopped")

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
        """ Register a job and add it to the job_queue as long as
            the ThreadPool is accepting jobs."""
        if not self.accepting_jobs:
            self.logger.info("Not accepting jobs - ThreadPool is shutting down.")
            return

        job = Job(job_id, data, type_command, self.logger)
        self.logger.info(f"Registered job with job_id: {job_id}")

        with self.lock:
            self.job_queue.put(job)
            self.job_list.append(job)


class TaskRunner(Thread):
    """ TaskRunner class is a thread that runs tasks from the job_queue. """
    def __init__(self, job_queue, lock, data_ingestor):
        super().__init__()
        self.job_queue = job_queue
        self.shutdown = Event()
        self.lock = lock
        self.data_ingestor = data_ingestor

    def run(self):
        """ Run task as long as the shutdown event is not set. """
        while not self.shutdown.is_set() or not self.job_queue.empty():
            # get the task from the queue, if available and execute it
            self.lock.acquire()

            if not self.job_queue.empty():
                job = self.job_queue.get()
                self.lock.release()
                job.run(self.data_ingestor)
            else:
                self.lock.release()
