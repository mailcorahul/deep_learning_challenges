import os

import cv2
import numpy as np
from PIL import Image
import torch
from torchvision import transforms
from torch.utils.data import Dataset



class ImageNet(Dataset):

    def __init__(self, root_dir, transform):
        self.root_dir = root_dir
        self.transform = transform

        self.image_paths = []
        files = os.listdir(self.root_dir)
        for file in files:
            self.image_paths.append(os.path.join(self.root_dir, file))

    
    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, index):
        image_path = self.image_paths[index]
        image = cv2.imread(image_path)[:,:,::-1]
        image = cv2.resize(image, (224, 224))
        image = np.transpose(image, (2, 0, 1))
        image = np.float32(image) / 255.
        image = torch.Tensor(image)
        image = self.transform(image)
        
        return image_path, image
