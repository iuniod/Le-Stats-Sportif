""" This module initializes the Flask application and read the data from the csv file. """
import os
import time
import logging
from flask import Flask
from app.data_ingestor import DataIngestor
from app.task_runner import ThreadPool
from logging.handlers import RotatingFileHandler

webserver = Flask(__name__)
webserver.tasks_runner = ThreadPool()

webserver.data_ingestor = DataIngestor("./nutrition_activity_obesity_usa_subset.csv")

if not os.path.exists('logs'):
    os.makedirs('logs')

webserver.logger = logging.Logger(__name__)
# Configure RotatingFileHandler to write to the log file "file.log"
# maximum log file size: 10KB, and keep 10 historical copies
handler = RotatingFileHandler("logs/file.log", maxBytes=10000, backupCount=10)
# Formatter for the log messages
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
handler.setFormatter(formatter)

webserver.logger.addHandler(handler)

webserver.logger.setLevel(logging.INFO)

webserver.tasks_runner.start(webserver.data_ingestor, webserver.logger)

webserver.job_counter = 1

if not os.path.exists('results'):
    os.makedirs('results')

from app import routes
