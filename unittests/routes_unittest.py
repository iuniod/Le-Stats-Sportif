""" Unit tests for the routes in the webserver module """
import unittest
from unittest.mock import patch
from app.job import Job
from app import webserver

class GracefulShutdownTest(unittest.TestCase):
    """ Unit tests for the graceful_shutdown route """
    @patch('app.webserver.tasks_runner.stop')
    def test_graceful_shutdown(self, mock_stop):
        """ Test that the route returns a success message when the server is shutting down """
        with webserver.test_client() as client:
            response = client.get('/api/graceful_shutdown')

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, {"status": "shutting down"})
            mock_stop.assert_called_once()

    @patch('app.webserver.tasks_runner.accepting_jobs', False)
    def test_graceful_shutdown_already_shutting_down(self):
        """ Test that the route returns an error if the server is already shutting down """
        with webserver.test_client() as client:
            response = client.get('/api/graceful_shutdown')

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, {"status": "error", \
                                             "reason": "Server is already shutting down"})

class NumJobsTest(unittest.TestCase):
    """ Unit tests for the num_jobs route """
    @patch('app.webserver.tasks_runner.job_queue.qsize', return_value=3)
    def test_num_jobs(self, mock_qsize):
        """ Test that the route returns the correct number of jobs """
        with webserver.test_client() as client:
            response = client.get('/api/num_jobs')

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, {"num_jobs": 3})
            mock_qsize.assert_called_once()

class JobsTest(unittest.TestCase):
    """ Unit tests for the jobs route """
    def test_jobs_empty(self):
        """ Test that the route returns an empty list when there are no jobs """
        with webserver.test_client() as client:
            response = client.get('/api/jobs')

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, [])

    @patch('app.webserver.tasks_runner.job_list')
    def test_jobs_not_empty(self, mock_job_list):
        """ Test that the route returns the correct job status """
        mock_job = Job(1, None, None)
        mock_job_list.return_value = [mock_job]

        with webserver.test_client() as client:
            response = client.get('/api/jobs')

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, [{"job_id": 1, "status": "running"}])
