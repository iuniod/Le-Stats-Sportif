""" This module initializes the Flask application and read the data from the csv file. """
import os
from flask import Flask
from app.data_ingestor import DataIngestor
from app.task_runner import ThreadPool
from app import routes

webserver = Flask(__name__)
webserver.tasks_runner = ThreadPool()

webserver.data_ingestor = DataIngestor("./nutrition_activity_obesity_usa_subset.csv")

webserver.tasks_runner.start(webserver.data_ingestor)

webserver.job_counter = 1

if not os.path.exists('results'):
    os.makedirs('results')
