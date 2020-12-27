import os
import redcap
import requests
import sys
import pandas as pd


def object_troubleshoot(obj):

    for attr in dir(obj):
        try:
            print("obj.%s = %r" % (attr, getattr(obj, attr)))
        except:
            pass

class UPDATE():

	def __init__(self, redcap_api_token=None, redcap_url=None):
		homedir = os.path.expanduser("~")
		api_keys = os.path.join(homedir, 'OneDrive - Ascension','Desktop','vax_api_keys.txt')

		if os.path.exists(api_keys) != True:
			api_keys = os.path.join(homedir, 'Desktop','vax_api_keys.txt')

		if os.path.exists(api_keys) != True:
			print('Can\'t find api keys file. Make sure it is on your desktop')

		with open(api_keys, 'r') as f:
			for i, line in enumerate(f):
				if i == 0:
					api_token = line.rstrip()

		self.redcap_url = 'https://redcap.ascension.org/txaus/api/'
		self.redcap_api_token = api_token
		

	def Data(self):
		'''
		API that pulls all data from Redcap
		'''
		
		api_key = self.redcap_api_token
		api_url = self.redcap_url

		project = redcap.Project(api_url, api_key)
		data = project.export_records()

		if len(data) > 0:
			print('deleting ' + str(len(data)) + ' records')
			dfData = pd.DataFrame.from_dict(data)
			records = dfData['record_id'].to_list()
			project.delete_records(records)
		else:
			print('No existing records to delete')

		thisPath = 'C:/Users/mrwilliams/My Stuff/vaxIntFace/data.xlsx'
		print('Getting new data')
		excelData = pd.read_excel('data.xlsx', sheet_name='Sheet1')
		# jsonData = excelData.to_json()
		print('Importing data')
		response = project.import_records(excelData)
		print(response)
		

if __name__ == '__main__':

	update = UPDATE()
	update.Data()