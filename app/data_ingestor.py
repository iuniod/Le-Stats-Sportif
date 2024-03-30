"""
This module is responsible for reading the csv file and storing the data in a
list of dictionaries.
"""
import csv

class DataIngestor:  # pylint: disable=too-few-public-methods
    """
    This class receives a csv file path and reads the data from the file.
    The data is stored in a list of dictionaries.
    """
    def __init__(self, csv_path: str):
        self.questions_best_is_min = [
            'Percent of adults aged 18 years and older who have an overweight classification',
            'Percent of adults aged 18 years and older who have obesity',
            'Percent of adults who engage in no leisure-time physical activity',
            'Percent of adults who report consuming fruit less than one time daily',
            'Percent of adults who report consuming vegetables less than one time daily'
        ]

        self.questions_best_is_max = [
            'Percent of adults who achieve at least 150 minutes a week of moderate-intensity \
                aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic \
                activity (or an equivalent combination)',
            'Percent of adults who achieve at least 150 minutes a week of moderate-intensity \
                aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic \
                physical activity and engage in muscle-strengthening activities on 2 or more \
                days a week',
            'Percent of adults who achieve at least 300 minutes a week of moderate-intensity \
                aerobic physical activity or 150 minutes a week of vigorous-intensity aerobic \
                activity (or an equivalent combination)',
            'Percent of adults who engage in muscle-strengthening activities on 2 or more days a \
                week',
        ]

        # read each row of the csv file and store it in a list of dictionaries
        self.data = []
        with open(csv_path, encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.data.append(row)
