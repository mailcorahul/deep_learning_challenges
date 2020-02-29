import sys
import os

from tqdm import tqdm
import pandas as pd

if __name__ == '__main__':

    csv_path = sys.argv[1]
    data_path = sys.argv[2]
    dest_path = sys.argv[3]
    os.makedirs(dest_path)
   
    ds = pd.read_csv(csv_path)

    print('[/] total number of rows: {}'.format(len(ds)))
    file2class = {}
    for i in range(len(ds)):
        file2class[ds.iloc[i]['Image']] = ds.iloc[i]['Class']

    print('[/] total number of unique image names: {}'.format(len(file2class)))

    files = os.listdir(data_path)
    print('[/] total number of files: {}'.format(len(files)))

    for file in tqdm(files):
        class_name = file2class[file]
        image_path = os.path.join(dest_path, class_name)
        os.makedirs(image_path, exist_ok=True)

        w = os.system('cp {}/{} {}'.format(data_path, file, image_path))

