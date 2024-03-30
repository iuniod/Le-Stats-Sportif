import unittest
import os
from app.task_runner import ThreadPool

 
class TestThreadPoolMethods(unittest.TestCase):
	def test_get_num_threads(self):
		"""
		This method tests the get_num_threads method of the ThreadPool class.
		"""
		# check if the env var is defined
		os.environ['TP_NUM_OF_THREADS'] = '5'
		tp = ThreadPool()
		self.assertEqual(tp.get_num_threads(), 5)

		# check if the env var is not defined
		os.environ.pop('TP_NUM_OF_THREADS')
		tp = ThreadPool()
		self.assertEqual(tp.get_num_threads(), os.cpu_count())

	def test_start(self):
		"""
		This method tests the start method of the ThreadPool class.
		"""
		tp = ThreadPool()
		tp.start()
		self.assertEqual(len(tp.tasks), tp.num_threads)
		self.assertEqual(tp.tasks[0].is_alive(), True)

		# close the threads
		tp.join()

	def test_join(self):
		"""
		This method tests the join method of the ThreadPool class.
		"""
		tp = ThreadPool()
		tp.start()
		tp.join()
		# check if all threads are closed
		for task in tp.tasks:
			self.assertEqual(task.is_alive(), False)