import json
import os
from pprint import pprint

SIZING_VALUE = 10
FILEPATH = './SemiConvertedData/'
NEWFILEPATH = './ConvertedGeoJsonFiles' + str(SIZING_VALUE) + 's/'

# File format.
# pprint(data['features'][0]['geometry']['coordinates'][0][0]

def rewriting_file_format(current_file, old_coordinates):
    new_coordinates = []
    starting_coordinates = []
    j = 0

    # Reordering and removing elements.
    for i in old_coordinates:
        if j == 0:
            starting_coordinates.append([i[1], i[0]])
        # Skip at every SIZING_VALUE
        if j % SIZING_VALUE == 0:
            new_coordinates.append([i[1], i[0]])
        j += 1
    
    print('')
    # Check last and starting coordinate is the same (requirement for polygons)
    if new_coordinates[len(new_coordinates)-1] != starting_coordinates[0]:
        new_coordinates.append([i[1], i[0]])

    # New geojson format.
    new_format = {
        'type': 'Feature',
        'properties': current_file,
        'geometry': {
            'type': 'Polygon',
            'coordinates': new_coordinates,
        }
    }

    # Write new converted file.
    with open(NEWFILEPATH + current_file, 'w') as outfile:
        json.dump(new_format, outfile)
    print('{} has been successfully reformatted.'.format(current_file))

def open_all_files_and_reformat():
    for current_file in os.listdir(os.getcwd() + FILEPATH):
        print(current_file)
        if current_file != 'northern-ireland.geojson':
            file_location = FILEPATH + current_file
            with open(file_location) as f:
                data = json.load(f)
                old_coordinates = data['features'][0]['geometry']['coordinates'][0][0]
                rewriting_file_format(current_file, old_coordinates)

open_all_files_and_reformat()