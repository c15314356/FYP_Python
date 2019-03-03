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


dataset_location = FILEPATH + 'crime_type_statistics.csv'
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
dataset = dataset.T
columns_names = ('Crime ID',
                'Month',
                'Reported by',
                'Falls within',
                'Longitude',
                'Latitude',
                'Location',
                'LSOA code',
                'LSOA name',
                'Crime type',
                'Last outcome category',
                'Context')

# for item in dataset:
#     print(dataset[item][0])
#     print(dataset[item][1])




def create_and_run_query():
    for item in dataset:
        query = session.execute_async(
            """
            insert into simple_crime_types(crime_type, count)
            VALUES (%s, %s)
            """,
            (str(dataset[item][0]), int(dataset[item][1]))
        )
        try:
            rows = query.result()
            print('executed insert')
        except Exception:
            logging.exception("Operation failed:")
    session.shutdown()
    return 'Import Successful'

create_and_run_query()