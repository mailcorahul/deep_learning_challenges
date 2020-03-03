import json
import sys

if __name__ == '__main__':

    mapping_path = sys.argv[1]
    input_path = sys.argv[2]
    dest_path = sys.argv[3]

    with open(mapping_path) as f:
        mapping = json.load(f)


    with open(input_path) as f:
        result = json.load(f)


    crops = result['crops']
    for i, crop in enumerate(crops):
        crops[i]['class'] = mapping[crops[i]['class']]

    with open(dest_path, 'w') as f:
        json.dump(result, f)

    
