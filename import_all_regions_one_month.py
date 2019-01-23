import logging
import pandas as pd
from cassandra.cluster import Cluster
import math
import os


FILEPATH = './data/2018-11/'

'''
CASSANDRA CONNECTION
'''
# Creating connection to cassandra and setting up session.
cluster = Cluster()
session = cluster.connect()
session.set_keyspace('crimes')

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
            query = session.execute_async(
                """
                insert into all_regions_one_month (id, latitude, longitude, location_details, crime_type, last_outcome)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (i, str(row[5]), str(row[4]), str(row[6]), str(row[9]), str(row[10]))
            )
            try:
                rows = query.result()
            except Exception:
                logging.exception("Operation failed:")

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
    session.shutdown()
    print('All files imported successfully.')


get_all_files_and_store_in_db()
