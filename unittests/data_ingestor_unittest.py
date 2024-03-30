"""
This module is responsible for testing the data_ingestor module.
"""
import unittest
import os
import app.data_ingestor as di

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
        di_list = di.DataIngestor(csv_path)

        # verify that the data is read correctly
        self.assertEqual(di_list.data, [{'name': 'Alice', 'age': '30'},
                                              {'name': 'Bob', 'age': '25'}])

        # remove the sample csv file
        os.remove(csv_path)

        # check for the main file if the data is read correctly
        di_list = di.DataIngestor('nutrition_activity_obesity_usa_subset.csv')

        self.assertEqual(len(di_list.data), 18650)
        data_entry = {'': '10730',
                        'YearStart': '2014',
                        'YearEnd': '2014',
                        'LocationAbbr': 'GU',
                        'LocationDesc': 'Guam',
                        'Datasource': 'Behavioral Risk Factor Surveillance System',
                        'Class': 'Obesity / Weight Status',
                        'Topic': 'Obesity / Weight Status',
                        'Question': 'Percent of adults aged 18 years and older who have obesity',
                        'Data_Value_Unit': '',
                        'Data_Value_Type': 'Value',
                        'Data_Value': '24.9',
                        'Data_Value_Alt': '24.9',
                        'Data_Value_Footnote_Symbol': '',
                        'Data_Value_Footnote': '',
                        'Low_Confidence_Limit': '17.9',
                        'High_Confidence_Limit ': '33.7',
                        'Sample_Size': '199.0',
                        'Total': '',
                        'Age(years)': '',
                        'Education': '',
                        'Gender': '',
                        'Income': 'Data not reported',
                        'Race/Ethnicity': '',
                        'GeoLocation': '(13.444304, 144.793731)',
                        'ClassID': 'OWS',
                        'TopicID': 'OWS1',
                        'QuestionID': 'Q036',
                        'DataValueTypeID': 'VALUE',
                        'LocationID': '66',
                        'StratificationCategory1': 'Income',
                        'Stratification1': 'Data not reported',
                        'StratificationCategoryId1': 'INC',
                        'StratificationID1': 'INCNR'
                    }
        self.assertEqual(di_list.data[10730], data_entry)
