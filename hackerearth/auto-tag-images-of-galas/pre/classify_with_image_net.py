import sys
import os
import json

from tqdm import tqdm
import cv2
import numpy as np
import torch
import torchvision
from torchvision import transforms, models

from dataset import ImageNet

if __name__ == '__main__':

    backbone_name = sys.argv[1]
    data_path = sys.argv[2]
    dest_path = sys.argv[3]

    with open("imagenet_class_index.json") as f:
        class_idx = json.load(f)
    idx2label = [class_idx[str(k)][1] for k in range(len(class_idx))]

    backbone = getattr(models, backbone_name)
    net = backbone(pretrained=True).cuda()

    batch_size = 128
    normalize = transforms.Normalize(
            mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]
        )

    image_data = ImageNet(root_dir=data_path, transform=normalize)
    data_loader = torch.utils.data.DataLoader(image_data, batch_size=128)

    for batch in tqdm(data_loader):
        batch_paths, batch_images = batch
        batch_images = batch_images.cuda()
        with torch.no_grad():
            batch_predictions = net(batch_images)
            _, max_predictions = torch.max(batch_predictions, dim=1)
            
            for i, class_idx in enumerate(max_predictions):
                try:
                    class_name = idx2label[class_idx]
                    dest_image_path = os.path.join(dest_path, class_name)
                    os.makedirs(dest_image_path, exist_ok=True)
                    os.system("cp '{}' '{}'".format(batch_paths[i], dest_image_path))
                except Exception as e:
                    print(e)

