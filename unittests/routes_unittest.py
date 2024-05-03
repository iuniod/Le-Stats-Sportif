""" Unit tests for the routes in the webserver module """
import unittest
import json
from unittest.mock import patch, MagicMock, Mock
from app.job import Job
from app import webserver, routes
from flask import request, jsonify, Response
from app.task_runner import ThreadPool

class TestRoutes(unittest.TestCase):
    """ This class is responsible for testing the routes in the webserver module """
    def setUp(self):
        """ Set up the test environment """
        webserver.data_ingestor = {
            "data": [
                {"" : 1, "LocationDesc": "Alabama", "Question": "Question1", "Data_Value": 10,
                "StratificationCategory1": "category1", "Stratification1": "stratification1"},
                {"" : 2, "LocationDesc": "Alaska", "Question": "Question1", "Data_Value": 20,
                "StratificationCategory1": "category1", "Stratification1": "stratification1"},
                {"" : 3, "LocationDesc": "Arizona", "Question": "Question1", "Data_Value": 30,
                "StratificationCategory1": "category1", "Stratification1": "stratification1"},
                {"" : 4, "LocationDesc": "Arkansas", "Question": "Question1", "Data_Value": 40,
                "StratificationCategory1": "category1", "Stratification1": "stratification1"},
                {"" : 5, "LocationDesc": "California", "Question": "Question1", "Data_Value": 50,
                "StratificationCategory1": "category1", "Stratification1": "stratification1"},

                {"" : 6, "LocationDesc": "Alabama", "Question": "Question1", "Data_Value": 11,
                "StratificationCategory1": "category1", "Stratification1": "stratification2"},
                {"" : 7, "LocationDesc": "Alaska", "Question": "Question1", "Data_Value": 21,
                "StratificationCategory1": "category1", "Stratification1": "stratification2"},
                {"" : 8, "LocationDesc": "Arizona", "Question": "Question1", "Data_Value": 31,
                "StratificationCategory1": "category1", "Stratification1": "stratification2"},
                {"" : 9, "LocationDesc": "Arkansas", "Question": "Question1", "Data_Value": 41,
                "StratificationCategory1": "category1", "Stratification1": "stratification2"},
                {"" : 10, "LocationDesc": "California", "Question": "Question1", "Data_Value": 51,
                "StratificationCategory1": "category1", "Stratification1": "stratification2"},
                
                {"" : 11, "LocationDesc": "Alabama", "Question": "Question1", "Data_Value": 60,
                "StratificationCategory1": "category2", "Stratification1": "stratification1"},
                {"" : 12, "LocationDesc": "Alaska", "Question": "Question1", "Data_Value": 70,
                "StratificationCategory1": "category2", "Stratification1": "stratification1"},
                {"" : 13, "LocationDesc": "Arizona", "Question": "Question1", "Data_Value": 80,
                "StratificationCategory1": "category2", "Stratification1": "stratification1"},
                {"" : 14, "LocationDesc": "Arkansas", "Question": "Question1", "Data_Value": 90,
                "StratificationCategory1": "category2", "Stratification1": "stratification1"},
                {"" : 15, "LocationDesc": "California", "Question": "Question1", "Data_Value": 100,
                "StratificationCategory1": "category2", "Stratification1": "stratification1"},

                {"" : 16, "LocationDesc": "Alabama", "Question": "Question1", "Data_Value": 61,
                "StratificationCategory1": "category2", "Stratification1": "stratification2"},
                {"" : 17, "LocationDesc": "Alaska", "Question": "Question1", "Data_Value": 71,
                "StratificationCategory1": "category2", "Stratification1": "stratification2"},
                {"" : 18, "LocationDesc": "Arizona", "Question": "Question1", "Data_Value": 81,
                "StratificationCategory1": "category2", "Stratification1": "stratification2"},
                {"" : 19, "LocationDesc": "Arkansas", "Question": "Question1", "Data_Value": 91,
                "StratificationCategory1": "category2", "Stratification1": "stratification2"},
                {"" : 20, "LocationDesc": "California", "Question": "Question1", "Data_Value": 101,
                "StratificationCategory1": "category2", "Stratification1": "stratification2"},

                {"" : 21, "LocationDesc": "Alabama", "Question": "Question2", "Data_Value": 10,
                "StratificationCategory1": "category1", "Stratification1": "stratification1"},
                {"" : 22, "LocationDesc": "Alaska", "Question": "Question2", "Data_Value": 20,
                "StratificationCategory1": "category1", "Stratification1": "stratification1"},
                {"" : 23, "LocationDesc": "Arizona", "Question": "Question2", "Data_Value": 30,
                "StratificationCategory1": "category1", "Stratification1": "stratification1"},
                {"" : 24, "LocationDesc": "Arkansas", "Question": "Question2", "Data_Value": 40,
                "StratificationCategory1": "category1", "Stratification1": "stratification1"},
                {"" : 25, "LocationDesc": "California", "Question": "Question2", "Data_Value": 50,
                "StratificationCategory1": "category1", "Stratification1": "stratification1"}
            ],
            "questions_best_is_min": ['Question1'],
            "questions_best_is_max": ['Question2']
        }
        webserver.tasks_runner = ThreadPool()
        webserver.logger = Mock()
        webserver.job_counter = 1
        webserver.tasks_runner.start(webserver.data_ingestor, webserver.logger)

    @patch('flask.jsonify')
    def test_get_response(self, jsonify_mock):
        """ Test the get_response function """
        jsonify_mock = lambda data, status_code=200: Response(json.dumps(data), status=status_code, mimetype='application/json')
        job = Job(1, {"question": "Question1", "state": "Alabama"}, "/api/state_mean", webserver.logger)
        job.result = 10
        webserver.tasks_runner.job_list.append(job)
        resp = routes.get_response("job_1")
        print(f"RESP: {resp}")
        # self.assertEqual(resp, jsonify({"status": "done", "data": 10}))