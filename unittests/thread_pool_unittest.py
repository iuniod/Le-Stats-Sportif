import unittest
import os
from app.task_runner import ThreadPool
from app.data_ingestor import DataIngestor
from app.job import Job
 
class TestThreadPoolMethods(unittest.TestCase):
	""" This class is responsible for testing the ThreadPool class."""
	def aux_data_ingestor(self):
		""" This method is used to create a sample csv file for data ingestor."""
		csv_path = 'sample.csv'

		with open(csv_path, 'w', encoding='utf-8') as file:
			file.write('name,age\n')
			file.write('Alice,30\n')
			file.write('Bob,25\n')

		di = DataIngestor(csv_path)

		# remove the sample csv file
		os.remove(csv_path)

		return di

	def aux_job(self):
		""" This method is used to create a sample job."""
		return Job(1, {'question' : 'Test'}, 'test')

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
		# create a sample csv file for data ingestor
		di_list = self.aux_data_ingestor()

		# start the threads and check if they are alive
		tp = ThreadPool()
		tp.start(di_list)
		self.assertEqual(len(tp.tasks), tp.num_threads)
		self.assertEqual(tp.tasks[0].is_alive(), True)

		# close the threads
		tp.join()

	def test_join(self):
		"""
		This method tests the join method of the ThreadPool class.
		"""
		di = self.aux_data_ingestor()
		tp = ThreadPool()
		tp.start(di)
		tp.join()
		# check if all threads are closed
		for task in tp.tasks:
			self.assertEqual(task.is_alive(), False)

	def test_register_job(self):
		"""
		This method tests the register_job method of the ThreadPool class.
		"""
		di = self.aux_data_ingestor()
		job = self.aux_job()
		tp = ThreadPool()
		tp.start(di)
		tp.register_job(job.job_id, job.input_data)
		self.assertEqual(tp.job_queue.qsize(), 1)
		self.assertEqual(tp.job_queue.get().job_id, job.job_id)
		self.assertEqual(tp.job_list[0].input_data, job.input_data)

		# close the threads
		tp.join()