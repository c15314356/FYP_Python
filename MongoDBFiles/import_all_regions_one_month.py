import pandas as pd
import pymongo
import os

FILEPATH = './data/2018-11/'

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
def create_and_run_query(dataset, lastid, filename):
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
        # print('| {} | {} | {} | {} | {} | {} |'.format(id, row[5], row[4], row[6], row[9], row[10]))
        # Checks that crime has a valid lat coord.
        if math.isnan(float(row[5])) == False:
            db.all_regions_one_month.insert_one({
                'location': {
                    'type': 'Point',
                    'coordinates': [str(row[4]), str(row[5])]
                },
                'properties': {
                    'crime_type': str(row[9]),
                    'crime_id': str(row[0])
                }
            })
            print('Executed insert. Current ID = {}  Current dataset = {}'.format(i, filename))
        i += 1
    print('Import succeeded')
    return i


def get_all_files_and_store_in_db():
    lastid = 0
    for filename in os.listdir(os.getcwd() + FILEPATH):
        if 'outcome' not in filename:
            print(filename)
            dataset_location = FILEPATH + filename
            dataset = pd.read_csv(dataset_location, header=None)
            lastid = create_and_run_query(dataset, lastid, filename)
    client.close()
    print('All files imported successfully.')


get_all_files_and_store_in_db()
