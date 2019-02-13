import json
import os
from pprint import pprint

FILEPATH = './OriginalData/SemiConvertedData/'
NEWFILEPATH = './ConvertedGeoJsonFilesMapboxFormat/'

# File format.
# pprint(data['features'][0]['geometry']['coordinates'][0][0]

def rewriting_file_format(current_file, old_coordinates):
    new_coordinates = []

    # Reordering and removing elements.
    for i in old_coordinates:
        new_coordinates.append([i[1], i[0]])


    # New geojson format.
    new_format = {
        'type': 'Polygon',
        'coordinates': new_coordinates
    }

    # Write new converted file.
    with open(NEWFILEPATH + current_file, 'w') as outfile:
        json.dump(new_format, outfile)
    print('{} has been successfully reformatted.'.format(current_file))

def open_all_files_and_reformat():
    for current_file in os.listdir(os.getcwd() + FILEPATH):
        print(current_file)
        file_location = FILEPATH + current_file
        with open(file_location) as f:
            data = json.load(f)
            old_coordinates = data['features'][0]['geometry']['coordinates'][0][0]
            rewriting_file_format(current_file, old_coordinates)

open_all_files_and_reformat()