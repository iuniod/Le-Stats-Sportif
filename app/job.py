""" This module contains the Job class which is used to store the job details.
    Job class has also a method to run the job.
"""
import json

class Job:  # pylint: disable=too-few-public-methods
    """ This class is used to store the job details and run the job."""
    def __init__(self, job_id, input_data, command):
        """ Initialize the Job class with job_id and input_data."""
        self.job_id = job_id
        self.input_data = input_data
        self.result = None
        self.status = "running"
        self.command = command

    def _states_mean(self, data_ingestor):
        # Extract relevant data entries for the specified question
        relevant_entries = [entry for entry in data_ingestor.data if entry['Question'] == self.input_data['question']]

        # Extract the state and the Data_Value column from the relevant data entries
        states_mean = {}
        for entry in relevant_entries:
            state = entry['LocationDesc']
            value = float(entry['Data_Value'])

            if state not in states_mean:
                states_mean[state] = []

            states_mean[state].append(value)

        # Calculate the mean of the Data_Value column for each state
        for state, values in states_mean.items():
            states_mean[state] = sum(values) / len(values)

        # Sort the dictionary by the mean of the Data_Value column
        states_mean = dict(sorted(states_mean.items(), key=lambda item: item[1]))

        # Make a json serializable object
        self.result = dict(states_mean)

    def _state_mean(self, data_ingestor):
        # Extract relevant data entries for the specified question
        relevant_entries = [entry for entry in data_ingestor.data if entry['Question'] == self.input_data['question'] and entry['LocationDesc'] == self.input_data['state']]

        # Calculate mean of the relevant data entries
        state_mean = sum([float(entry['Data_Value']) for entry in relevant_entries]) / len(relevant_entries)

        # Make a json serializable object
        self.result = {self.input_data['state']: state_mean}

    def _global_mean(self, data_ingestor):
        # Extract relevant data entries for the specified question
        relevant_entries = [float(entry['Data_Value']) for entry in data_ingestor.data if entry['Question'] == self.input_data['question']]

        # Calculate mean of the relevant data entries
        global_mean = sum(relevant_entries) / len(relevant_entries)

        # Make a json serializable object
        self.result = {"global_mean": global_mean}

    def _diff_from_mean(self, data_ingestor):
        # Get for each state the mean of the Data_Value column for the specified question
        # and store it in a variable
        self._states_mean(data_ingestor)
        states_mean = self.result

        # Get the global mean of the Data_Value column for the specified question
        # and store it in a variable
        self._global_mean(data_ingestor)
        global_mean = self.result["global_mean"]

        # Calculate the difference between the mean of the Data_Value column for each state
        # and the global mean of the Data_Value column
        diff_from_mean = {state: global_mean - mean for state, mean in states_mean.items()}

        # Make a json serializable object
        self.result = diff_from_mean

    def _state_diff_from_mean(self, data_ingestor):
        # Get the mean of the Data_Value column for the specified question and state,
        # and store it in a variable
        self._state_mean(data_ingestor)
        state_mean = self.result[self.input_data['state']]
        state_name = self.input_data['state']

        # Get the global mean of the Data_Value column for the specified question
        # and store it in a variable
        self._global_mean(data_ingestor)
        global_mean = self.result["global_mean"]

        # Calculate the difference between the mean of the Data_Value column for the specified state
        # and the global mean of the Data_Value column
        state_diff_from_mean = global_mean - state_mean

        # Make a json serializable object
        self.result = {state_name: state_diff_from_mean}

    def _default(self, data_ingestor):
        print("This is the default case")

    def _switch_case(self, data_ingestor):
        switch = {
            '/api/states_mean': self._states_mean,
            '/api/global_mean': self._global_mean,
            '/api/state_mean': self._state_mean,
            '/api/diff_from_mean': self._diff_from_mean,
            '/api/state_diff_from_mean': self._state_diff_from_mean,
        }

        func = switch.get(self.command, self._default)
        func(data_ingestor)

    def run(self, data_ingestor):
        """ Run the job according to the command of the job."""
        # find result based on the command
        self._switch_case(data_ingestor)

        # write the result to a file in results folder, with the job_id as the filename
        with open(f"results/job_id{self.job_id}.json", 'w', encoding='utf-8') as f:
            f.write(json.dumps(self.result))

        # Update the status of the job
        self.status = "done"
