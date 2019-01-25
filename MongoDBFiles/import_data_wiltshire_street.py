import logging
import pandas as pd
import pymongo

import math

FILEPATH = './data/'

'''
MONGODB CONNECTION
'''
#Creation of Mongodb Client
client = pymongo.MongoClient("localhost", 27017)
#creates + connects to GameOfThronesCollection
db = client.CrimeExplorerDB

dataset_location = FILEPATH + '2018-11-wiltshire-street.csv'
dataset = pd.read_csv(dataset_location, header=None)

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


def create_and_run_query():
    dataset_no_cols = dataset.iloc[1:]
    i = 1
    for index, row in dataset_no_cols.iterrows():
        # print('| {} | {} | {} | {} | {} | {} |'.format(id, row[5], row[4], row[6], row[9], row[10]))
        # Checks that crime has a valid lat coord
        if math.isnan(float(row[5])) == False:
            db.wiltshire_street.insert_one({
                'location': {
                    'type': 'Point',
                    'coordinates': [str(row[4]), str(row[5])]
                },
                'properties': {
                    'crime_type': str(row[9]),
                    'crime_id': str(row[0])
                }
            })
            print('executed insert')
        i += 1
    client.close()
    print('All files imported successfully.')


create_and_run_query()