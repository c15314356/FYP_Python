import json
import pymongo
import os

FILEPATH = './KMLGeoJsonFiles/ConvertedGeoJsonFiles/'

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
def open_all_files_and_import_to_db():
    for filename in os.listdir(os.getcwd() + FILEPATH):
        file_location = FILEPATH + filename
        print('Opening {}...'.format(filename))
        with open(file_location) as f:
            data = json.load(f)
            db.region_coordinates.insert_one(data)
            print('{} was succesfully imported into Mongo DB.'.format(filename))
    client.close()
    print('All files imported successfully.')


open_all_files_and_import_to_db()
