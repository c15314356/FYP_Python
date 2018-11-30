import logging
import pandas as pd
from cassandra.cluster import Cluster
import math

FILEPATH = './data/'

'''
CASSANDRA CONNECTION
'''
# Creating connection to cassandra and setting up session
cluster = Cluster()
session = cluster.connect()
session.set_keyspace('crimes')


dataset_location = FILEPATH + '2017-01-city-of-london-street.csv'
dataset = pd.read_csv(dataset_location, header=None)

'''
Structure of dataframe
Crime ID    0
Month	 1
Reported by	Falls within	2
Longitude	 3
Latitude	 4
Location	 5
LSOA code	 6
LSOA name	 7
Crime type	 8
Last outcome category	 9
Context	    10
'''

def create_and_run_query():
    dataset_no_cols = dataset.iloc[1:]
    i = 1
    for index, row in dataset_no_cols.iterrows():
        # print('| {} | {} | {} | {} | {} | {} |'.format(id, row[5], row[4], row[6], row[9], row[10]))
        # Checks that crime has a valid lat coord
        if math.isnan(float(row[5])) == False:
            query = session.execute_async(
                """
                insert into general_crimes (id, latitude, longitude, location_details, crime_type, last_outcome)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (i, str(row[5]), str(row[4]), str(row[6]), str(row[9]), str(row[10]))
            )
            try:
                rows = query.result()
            except Exception:
                logging.exception("Operation failed:")

            print('executed insert')
        i += 1
    session.shutdown()
    return 'Import Successful'

create_and_run_query()
