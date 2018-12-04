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
                
crime_statistics = dataset.describe()
crime_statistics.columns = columns_names
crime_statistics = crime_statistics.T

crime_statistics.to_csv(FILEPATH + 'crime_statistics.csv', encoding='utf-8')
print(crime_statistics)
