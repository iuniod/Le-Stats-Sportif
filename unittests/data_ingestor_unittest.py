"""
This module is responsible for testing the data_ingestor module.
"""
import unittest
import os
from app.data_ingestor import DataIngestor

class TestDataIngestor(unittest.TestCase):
    """
    This class is responsible for testing the DataIngestor class.
    """
    def test_ingest_data(self):
        """
        This method tests the ___init___ method of the DataIngestor class.
        """
        # create a sample csv file
        csv_path = 'sample.csv'

        with open(csv_path, 'w', encoding='utf-8') as file:
            file.write('name,age\n')
            file.write('Alice,30\n')
            file.write('Bob,25\n')

        # run data ingestor
        di_list = DataIngestor(csv_path)

        # verify that the data is read correctly
        self.assertEqual(di_list.data, [{'name': 'Alice', 'age': '30'},
                                              {'name': 'Bob', 'age': '25'}])

        # remove the sample csv file
        os.remove(csv_path)

        # check for the main file if the data is read correctly
        di_list = DataIngestor('nutrition_activity_obesity_usa_subset.csv')

        self.assertEqual(len(di_list.data), 18650)
        data_entry = {'': '10730',
                        'LocationDesc': 'Guam',
                        'Question': 'Percent of adults aged 18 years and older who have obesity',
                        'Data_Value': '24.9',
                        'StratificationCategory1': 'Income',
                        'Stratification1': 'Data not reported',
                    }
        self.assertEqual(di_list.data[10730], data_entry)
