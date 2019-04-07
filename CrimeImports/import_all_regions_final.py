import pandas as pd
import pymongo
import math
import os

FILEPATH = './data/2015-2018'

'''
MONGODB CONNECTION
'''
#Creation of Mongodb Client.
client = pymongo.MongoClient("localhost", 27017)
#creates + connects to CrimeExplorerDB.
db = client.CrimeExplorerDB

'''
METHODS
'''
# Creates a query using a dataset which will import line by line from the dataset.
def create_and_run_query(dataset, lastid, file_name):
    '''
    Structure of dataframe
    Crime ID    0
    Month	 1
    Reported by	2
    Falls within	3
    Longitude	 4
    Latitude	 5
    Location	 6
    LSOA code	 7
    LSOA name	 8
    Crime type	 9
    Last outcome category	 10
    Context	    11
    '''
    dataset_no_cols = dataset.iloc[1:]
    i = 1 + lastid
    for index, row in dataset_no_cols.iterrows():
        # Checks that crime has a valid lat coord.
        if math.isnan(float(row[5])) == False:
            # Inserts data into collection by using the file name
            db[file_name].insert_one({
                'location': {
                    'type': 'Point',
                    'coordinates': [str(row[4]), str(row[5])]
                },
                'properties': {
                    'crime_type': str(row[9]),
                    'crime_id': str(row[0]),
                    'crime_date': str(row[1])
                }
            })
            print('Executed insert. Current ID = {}  Current dataset = {}'.format(i, file_name))
        i += 1
    print('Import succeeded')
    return i


'''
Remove the first 8 characters and the last 11 reformating 
Filenames from: 2018-10-wiltshire-street.csv --> wiltshire
This is is used to allow the ability to use the filename as database collection
'''
def file_name_cleaner(file_name):
   return file_name[8:len(file_name)-11]


def get_all_files_and_store_in_db():
    lastid = 0
    for file_directory in os.listdir(os.getcwd() + FILEPATH):
        for file_name in os.listdir(os.getcwd() + FILEPATH + file_directory):
            if 'outcome' not in file_name:
                clean_file_name = file_name_cleaner(file_name)
                print('{}'.format(file_name))
                dataset_location = os.getcwd() + FILEPATH + file_directory + '/' + file_name
                print(dataset_location)
                dataset = pd.read_csv(dataset_location, header=None)
                lastid = create_and_run_query(dataset, lastid, clean_file_name)
    client.close()
    print('All files imported successfully.')


get_all_files_and_store_in_db()
