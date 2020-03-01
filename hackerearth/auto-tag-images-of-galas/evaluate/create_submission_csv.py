import json
import os
import sys

if __name__ == '__main__':

    result_path = sys.argv[1]
    csv_path = sys.argv[2]

    with open(result_path) as f:
        result = json.load(f)

    csv_str = "Image,Class"
    crops = result["crops"]
    for crop in crops:
        image_name = crop["id"] + ".jpg"
        class_name = crop["class"]
        row = "\n{},{}".format(image_name, class_name)
        csv_str += row

    with open(csv_path, 'w') as f:
        f.write(csv_str)
