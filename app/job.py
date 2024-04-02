""" This module contains the Job class which is used to store the job details.
	Job class has also a method to run the job.
"""
import json

class Job:
	def __init__(self, job_id, input_data, type):
		""" Initialize the Job class with job_id and input_data."""
		self.job_id = job_id
		self.input_data = input_data
		self.result = None
		self.status = "running"
		self.type = type

	def _states_mean(self, data_ingestor):
		# Create a dictionary to store the mean of the Data_Value column
		states_mean = {}
		states_sum = {}
		states_count = {}

		# Iterate over the data
		for entry in data_ingestor.data:
			state = entry['LocationDesc']
			value = float(entry['Data_Value'])
			question = entry['Question']
			year_start = int(entry['YearStart'])
			year_end = int(entry['YearEnd'])

			# Check if the state is already in the dictionary
			if question == self.input_data['question'] and 2011 <= year_start <= 2022 and 2011 <= year_end <= 2022:
				if state not in states_sum:
					states_sum[state] = 0
					states_count[state] = 0
				
				states_sum[state] += value
				states_count[state] += 1

		# Calculate the mean of the Data_Value column for each state
		for state in states_sum:
			states_mean[state] = states_sum[state] / states_count[state]

		# Sort the dictionary by the mean of the Data_Value column
		states_mean = dict(sorted(states_mean.items(), key=lambda item: item[1]))

		# Make a json serializable object
		self.result = {k: v for k, v in states_mean.items()}
		a = self.result
		j = json.dumps(a)

		# write the result to a file in results folder, with the job_id as the filename
		with open(f"results/job_id{self.job_id}.json", 'w') as f:
			f.write(j)
		
		# Update the status of the job
		self.status = "done"


	def _default(self, data_ingestor):
		print("This is the default case")

	def _switch_case(self, data_ingestor):
		switch = {
			'/api/states_mean': self._states_mean,
		}
		
		func = switch.get(self.type, self._default)
		func(data_ingestor)

	def run(self, data_ingestor):
		""" Run the job according to the type of the job."""
		self._switch_case(data_ingestor)